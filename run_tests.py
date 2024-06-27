"""
:file: run_tests.py

:date: 2024/06/25
:author: Bryan Gillis

Entry-point file to run the interface and unit tests
"""

import json
import os
import sys
import tempfile

import subprocess
from PySide6 import QtCore, QtWidgets

class MyWidget(QtWidgets.QWidget):
  def __init__(self, test_module):
    super().__init__()

    self.test_module = test_module

    self.layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self)

    self.left_layout = QtWidgets.QVBoxLayout()
    self.right_layout = QtWidgets.QVBoxLayout()

    self.layout.addLayout(self.left_layout)
    self.layout.addLayout(self.right_layout)

    self.input_layout = QtWidgets.QFormLayout()
    self.l_inputs = []
    for i in range(5):
      label_widget = QtWidgets.QLabel(f"Test value {i}:")

      text_edit_widget = QtWidgets.QLineEdit()
      self.l_inputs.append(text_edit_widget)

      self.input_layout.addRow(label_widget, text_edit_widget)

    self.left_layout.addLayout(self.input_layout)

    self.text = QtWidgets.QLabel("Press the button to run the unit tests!")
    self.left_layout.addWidget(self.text)

    self.button = QtWidgets.QPushButton("Click me!")
    self.button.clicked.connect(self.run_tests)
    self.left_layout.addWidget(self.button)

    self.results_label = QtWidgets.QLabel("")

    self.summary_layout = QtWidgets.QFormLayout()

    self.first_run = True

  @QtCore.Slot()
  def run_tests(self):

    l_input = [None] * 5
    for i in range(5):
      l_input[i] = self.l_inputs[i].text()
    l_input = [x for x in l_input if x!=""]
    if len(l_input)==0:
      test_values = [0, 2, 4, 1.5]
    else:
      test_values = l_input

    # Create a temporary JSON file for output
    tmp_json = tempfile.NamedTemporaryFile(delete=False)
    d_results = {}
    try:
      # Call pytest on the test module
      subprocess.run([sys.executable, "-m", "pytest", f"--json={tmp_json.name}", self.test_module, "--test_values",
                      *map(str,test_values)], capture_output=True)
      d_results = json.load(open(tmp_json.name,'r'))
    finally:
        tmp_json.close()

    if len(d_results)==0:
      self.results_label.setText("Tests failed to run")
      return
    d_report = d_results['report']
    self.results_label.setText("Tests complete!")
    if self.first_run:
      self.left_layout.addWidget(self.results_label)
      self.left_layout.addLayout(self.summary_layout)
      self.first_run = False

    # Add a section to summarize test results (after cleaning up any existing one)
    d_summary = d_report['summary']
    while self.summary_layout.count():
      child = self.summary_layout.takeAt(0)
      child_widget = child.widget()
      if child_widget is not None:
          child_widget.deleteLater()
    self.summary_layout.addRow(QtWidgets.QLabel('Tests passed:'),
                               QtWidgets.QLabel(f"{d_summary['passed']}/{d_summary['num_tests']}"))
    self.summary_layout.addRow(QtWidgets.QLabel('Tests failed:'),
                               QtWidgets.QLabel(f"{d_summary['failed']}/{d_summary['num_tests']}"))
    self.summary_layout.addRow(QtWidgets.QLabel('Tests skipped:'),
                               QtWidgets.QLabel(f"{d_summary['skipped']}/{d_summary['num_tests']}"))
    
    # Clean up results from any previous test runs
    while self.right_layout.count():
      child = self.right_layout.takeAt(0)
      child_widget = child.widget()
      if child_widget is not None:
          child_widget.deleteLater()
      else:
        while child.count():
          child_child = child.takeAt(0)
          child_child_widget = child_child.widget()
          if child_child_widget is not None:
              child_child_widget.deleteLater()

    for d_test in d_report['tests']:
      test_layout = QtWidgets.QVBoxLayout()
      self.right_layout.addLayout(test_layout)
      test_layout.addWidget(QtWidgets.QLabel(d_test['name']))

      # Color the test result accordingly with its result
      test_outcome = d_test['outcome']
      outcome_color="black"
      if test_outcome=="passed":
        outcome_color="green"
      elif test_outcome=="failed":
        outcome_color="red"
      elif test_outcome=="skipped":
        outcome_color="blue" 

      test_layout.addWidget(QtWidgets.QLabel(f"Result: <span style='font-weight:900; color:{outcome_color};'>"
                                             f"{test_outcome.upper()}</span>"))

      # If a detailed report is present, add it in a QTextEdit
      d_call = d_test.get('call')
      if not d_call:
        continue
      test_report_str = d_call.get('longrepr')
      if not test_report_str:
        continue
      test_report = QtWidgets.QTextEdit(test_report_str)
      test_report.setReadOnly(True)
      test_layout.addWidget(test_report)


    
    self.resize(800,600)


if __name__ == "__main__":

  # Get the path to the test module
  file_path = os.path.split(os.path.realpath(__file__))[0]
  tests_path = os.path.join(file_path,"tests/python")
  test_module = os.path.join(tests_path,"test_values.py")

  app = QtWidgets.QApplication([])

  widget = MyWidget(test_module=test_module)
  widget.show()

  sys.exit(app.exec())