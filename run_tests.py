"""
:file: run_tests.py

:date: 2024/06/25
:author: Bryan Gillis

Executable python script which displays a widget to allow running of unit tests (optionally with custom values to test
a function on) and display results.
"""

import json
import os
import subprocess
import sys
import tempfile

from PySide6 import QtCore, QtWidgets

DEFAULT_NUM_USER_VALUES = 5

class TestRunnerWidget(QtWidgets.QWidget):
    """A Qt-based which which when shown will provide an interface to run unit tests and display the results.
    """
    def __init__(self, test_module, num_user_values = DEFAULT_NUM_USER_VALUES):
        super().__init__()

        self.test_module = test_module
        self.num_user_values = num_user_values

        self.layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self)

        self.left_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()

        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)

        self.input_layout = QtWidgets.QFormLayout()
        self.l_inputs = []
        for i in range(self.num_user_values):
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

    def cleanup(self):
        """Clean up any previous test results from the widget. Note that this isn't a full implementation which can
        clean up arbitrary layouts and widgets, which would necessarily be recursive. This goes only to the depth
        necessary to clean up what exists in this widget.
        """

        # Clean up any prior results
        while self.summary_layout.count():
            child = self.summary_layout.takeAt(0)
            child_widget = child.widget()
            if child_widget is not None:
                child_widget.deleteLater()

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

    @QtCore.Slot()
    def run_tests(self):
        """Method called when the widget's button is pressed, which cleans up any previous test results, runs the tests,
        and displays the results.
        """

        self.cleanup()

        # Get any user values supplied. Any empty boxes are removed from the list
        # We don't use self.num_user_values here just in case self.l_inputs has changed (due to future code changes)
        num_user_values = len(self.l_inputs)
        l_input_values = [None] * num_user_values
        for i in range(num_user_values):
            l_input_values[i] = self.l_inputs[i].text()
        l_input_values = [x for x in l_input_values if x!=""]

        # If the list is ultimately empty, use a default set which all passes
        if len(l_input_values)==0:
            l_input_values = [0, 2, 4, 1.5]

        self.results_label.setText("Tests running...")
        if self.first_run:
            self.left_layout.addWidget(self.results_label)
            self.left_layout.addLayout(self.summary_layout)
            self.first_run = False

        # Create a temporary JSON file for output
        tmp_json = tempfile.NamedTemporaryFile(delete=False)
        d_results = {}
        try:
            # Call pytest on the test module
            subprocess.run([sys.executable, "-m", "pytest", f"--json={tmp_json.name}", self.test_module,
                            "--test_values", *map(str,l_input_values)], capture_output=True, check=True)
            d_results = json.load(open(tmp_json.name,'r'))
        except Exception:
            self.results_label.setText("Tests failed to run")
        finally:
            tmp_json.close()
            os.unlink(tmp_json.name)

        if len(d_results)==0:
            self.results_label.setText("Tests failed to run")
            return
        d_report = d_results['report']
        self.results_label.setText("Tests complete!")

        # Add a section to summarize test results
        d_summary = d_report['summary']
        self.summary_layout.addRow(QtWidgets.QLabel('Tests passed:'),
                                  QtWidgets.QLabel(f"{d_summary['passed']}/{d_summary['num_tests']}"))
        self.summary_layout.addRow(QtWidgets.QLabel('Tests failed:'),
                                  QtWidgets.QLabel(f"{d_summary['failed']}/{d_summary['num_tests']}"))
        self.summary_layout.addRow(QtWidgets.QLabel('Tests skipped:'),
                                  QtWidgets.QLabel(f"{d_summary['skipped']}/{d_summary['num_tests']}"))

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

    widget = TestRunnerWidget(test_module=test_module)
    widget.show()

    sys.exit(app.exec())
