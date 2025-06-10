"""Run Pylint on all modules and display results."""
import subprocess
from pathlib import Path
import sys


def run_pylint(module_path):
    """Run pylint on a module and return the score."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pylint", "--output-format=text", module_path],
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout
        # Extract score from Pylint output
        score_line = [line for line in output.split('\n') if "Your code has been rated at" in line]
        if score_line:
            score_str = score_line[0].split()[6].split('/')[0]  # Get the numeric part before '/10'
            try:
                score = float(score_str)
                return score, output
            except ValueError:
                return None, output
        return None, output
    except FileNotFoundError:
        return None, "Pylint not installed"


def display_pylint_results():
    """Run Pylint on all modules and display results."""
    modules = [
        "run_time/data_aquisition.py",
        "run_time/data_cleaning_etc.py",
        "server_data/cne_server.py",
        "run_time/requirements.py",
        "src/file_handlers.py",
        "src/data_generator.py",
        "unit_tests/0_requirements_test.py",
        "unit_tests/1_file_handlers_test.py",
        "unit_tests/2_data_aquisition_test.py",
        "unit_tests/3_data_generator_test.py",
        "unit_tests/4_cne_server_test.py",
        "unit_tests/run_all_tests.py",
        "unit_tests/run_pylint.py",
    ]
    print("\n" + "=" * 50)
    print("PYLINT CODE ANALYSIS RESULTS")
    print("=" * 50)
    max_len = max(len(module) for module in modules)
    scores = []
    for module in modules:
        module_path = Path(module)
        if module_path.exists():
            score, output = run_pylint(str(module_path))
            if score is not None:
                print(f"{module.ljust(max_len)} : {score}/10")
                scores.append(score)
            else:
                print(f"{module.ljust(max_len)} : Score not available")
                # Uncomment to show full Pylint output:
                # print(output)
        else:
            print(f"{module.ljust(max_len)} : File not found")
    if scores:
        average_score = sum(scores) / len(scores)
        print("=" * 50)
        print(f"AVERAGE SCORE: {average_score:.2f}/10")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    display_pylint_results()
    
