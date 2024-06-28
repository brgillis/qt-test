# QT-Test

This is a learning project for me to learn QT and test/demonstrate my basic understanding of it by creating a small
program run in a QT window. The program runs unit tests of a mock function and reports the results in the window when
a button is pressed. The user can input specific values to test the mock function on, and one of the tests is set up
to use the user-provided values if any are provided.

Credit to the QT quick-start guide at https://doc.qt.io/qtforpython-6/quickstart.html, and miscellaneous other QT
resources around the web.


## Contributors


### Active Contributors

* Bryan Gillis (7204836+brgillis@users.noreply.github.com)


### Other Contributors



## Requirements

This project uses the following packages, with the versions it has been tested with listed here. Other versions will
likely work, but have not been tested.

* Python 3.11.6
* PySide6 6.7.2 (The python implementation of Qt)
* pytest 8.2.82


## Execution

This project can be executed by calling the `run_tests.py` script with a python interpreter, e.g. `python run_tests.py`.

This will cause a window to appear. Execution can be halted at any time by closing the window. This window presents a
button with the text "Click me!" Clicking on the button will result in a call to `pytest` on this project's unit tests.
A summary of the results will appear below the button, and details of the results will appear in a new panel to the
right.

Above the button, the user can supply 0 to 5 values which they wish to test the mock function on. The mock function
being tested is a naive implementation of a floor function (rounding a number down to the nearest integer lower than
it), which implements this by casting the value to an integer. The fourth unit test checks that the results of this mock
function match those of python's built-in `math.floor` function, and will fail if the results don't match for any
provided value, and will succeed if they all do match. All other unit tests use fixed values regardless of user input.

This implementation succeeds for all positive values, but fails for all negative non-integer values, which can be
confirmed by inputting a test value such as -1.5 in one of the boxes. The test will also fail on NaN or on any string
which cannot be converted to a number.


## Project Structure

* `tests`
  * `python`
    * `conftest.py` - Python file containing code used commonly by tests when run with `pytest`
    * `test_values.py` - Python file containing definition of a mock function and mock tests of it
* `README.md` - This file
* `run_tests.py` - Executable python script which provides a window to run unit tests and see the results
