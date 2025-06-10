"""Run all unit tests in the specified order and display Pylint results."""
import sys
import os
from pathlib import Path
import unittest
import platform
import time


import run_pylint as pylint_module # pylint: disable=import-error, wrong-import-position

def clear_terminal():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Linux and macOS
        os.system('clear')

def get_ordered_test_cases():
    """Return test cases in the desired execution order."""
    return [
        '0_requirements_test',
        '1_file_handlers_test',
        '2_data_aquisition_test',
        '3_data_generator_test',
        '4_cne_server_test'
    ]

def run_all_tests():
    """Run all unit tests in the test directory in specified order."""
    test_dir = Path(__file__).parent
    sys.path.append(str(test_dir.parent))
    loader = unittest.TestLoader()
    # Create a test suite with tests in specified order
    suite = unittest.TestSuite()
    for test_case in get_ordered_test_cases():
        try:
            module = __import__(test_case)
            tests = loader.loadTestsFromModule(module)
            suite.addTests(tests)
        except ImportError as e:
            print(f"Could not import {test_case}: {e}")
            sys.exit(1)
    runner = unittest.TextTestRunner(verbosity=0)
    clear_terminal()
    # Measure execution time
    start_time = time.time()
    result = runner.run(suite)
    elapsed_time = time.time() - start_time

    # Print test results
    if result.wasSuccessful():
        clear_terminal()
        print(f"Ran {result.testsRun} tests in {elapsed_time:.3f}s")
        print("OK\nAll tests passed successfully!")
    else:
        print("Some tests failed.")
        sys.exit(1)
    # Display Pylint results after tests
    pylint_module.display_pylint_results()

if __name__ == "__main__":
    run_all_tests()
