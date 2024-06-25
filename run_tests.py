"""
:file: run_tests.py

:date: 2024/06/25
:author: Bryan Gillis

Entry-point file to run the interface and unit tests
"""

import os
import sys

import pytest
from PySide6 import QtCore, QtWidgets

class MyWidget(QtWidgets.QWidget):
  def __init__(self, test_module):
    super().__init__()

    self.test_module = test_module

    self.button = QtWidgets.QPushButton("Click me!")
    self.text = QtWidgets.QLabel("Press the button to run the unit tests!",
                                 alignment=QtCore.Qt.AlignCenter)
    
    self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
    self.layout.addWidget(self.text)
    self.layout.addWidget(self.button)

    self.button.clicked.connect(self.run_tests)

  @QtCore.Slot()
  def run_tests(self):

    # TODO - Replace the next bit with use of QT to make an interface to get values and call pytest with them
    test_values = [0, 2, 4, 1.5, -1.5]

    # Call pytest on the test module
    pytest.main([self.test_module, "--test_values", *map(str,test_values)])

if __name__ == "__main__":

  # Get the path to the test module
  file_path = os.path.split(os.path.realpath(__file__))[0]
  tests_path = os.path.join(file_path,"tests/python")
  test_module = os.path.join(tests_path,"test_values.py")

  app = QtWidgets.QApplication([])

  widget = MyWidget(test_module=test_module)
  widget.resize(800,600)
  widget.show()

  sys.exit(app.exec())