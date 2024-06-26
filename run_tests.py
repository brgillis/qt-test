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

    self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)

    self.input_layout = QtWidgets.QFormLayout(self)
    self.l_inputs = []
    for i in range(5):
      label_widget = QtWidgets.QLabel(f"Test value {i}:")

      text_edit_widget = QtWidgets.QLineEdit()
      self.l_inputs.append(text_edit_widget)

      self.input_layout.addRow(label_widget, text_edit_widget)

    self.layout.addLayout(self.input_layout)

    self.text = QtWidgets.QLabel("Press the button to run the unit tests!",
                                 alignment=QtCore.Qt.AlignCenter)
    self.layout.addWidget(self.text)

    self.button = QtWidgets.QPushButton("Click me!")
    self.button.clicked.connect(self.run_tests)
    self.layout.addWidget(self.button)

    self.results_text = QtWidgets.QTextEdit("", alignment=QtCore.Qt.AlignLeft)
    self.results_text.setReadOnly(True)



  @QtCore.Slot()
  def run_tests(self):

    l_input = [None] * 5
    for i in range(5):
      l_input[i] = self.l_inputs[i].text()
    l_input = [x for x in l_input if x!=""]
    if len(l_input)==0:
      test_values = [0, 2, 4, 1.5, -1.5]
    else:
      test_values = l_input

    # Create a temporary JSON file for output
    tmp_json = tempfile.NamedTemporaryFile(delete=False)
    try:
      # Call pytest on the test module
      subprocess.run([sys.executable, "-m", "pytest", f"--json={tmp_json.name}", self.test_module, "--test_values",
                      *map(str,test_values)], capture_output=True)
      d_results = json.load(open(tmp_json.name,'r'))
      self.results_text.setText("Tests complete!\n" + repr(d_results))
      self.layout.addWidget(self.results_text)
      self.resize(800,600)
    finally:
        tmp_json.close()

if __name__ == "__main__":

  # Get the path to the test module
  file_path = os.path.split(os.path.realpath(__file__))[0]
  tests_path = os.path.join(file_path,"tests/python")
  test_module = os.path.join(tests_path,"test_values.py")

  app = QtWidgets.QApplication([])

  widget = MyWidget(test_module=test_module)
  widget.show()

  sys.exit(app.exec())