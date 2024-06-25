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

    self.text = QtWidgets.QLabel("Press the button to run the unit tests!",
                                 alignment=QtCore.Qt.AlignCenter)
    self.layout.addWidget(self.text)

    self.button = QtWidgets.QPushButton("Click me!")
    self.layout.addWidget(self.button)

    self.results_visible = False
    self.results_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignLeft)

    self.button.clicked.connect(self.run_tests)

  @QtCore.Slot()
  def run_tests(self):

    # TODO - Replace the next bit with use of QT to make an interface to get values and call pytest with them
    test_values = [0, 2, 4, 1.5, -1.5]

    # Create a temporary JSON file for output
    tmp_json = tempfile.NamedTemporaryFile(delete=False)
    try:
      # Call pytest on the test module
      subprocess.run([sys.executable, "-m", "pytest", f"--{tmp_json.name}", self.test_module, "--test_values",
                      *map(str,test_values)], capture_output=True)
      import pdb; pdb.set_trace()
      d_results = json.load(open(tmp_json.name,'r'))
      self.results_label.setText("Tests complete!\n" + repr(d_results))
      self.layout.addWidget(self.results_label)
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