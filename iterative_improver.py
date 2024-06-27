from test_runner import TestRunner
from ai_interaction import AIInteraction

class IterativeImprover:
    """
    A class to handle iterative improvement of the generated code by running tests and fixing errors.
    """

    def __init__(self, project_name):
        """
        Initialize the IterativeImprover with the project name.
        
        Args:
            project_name (str): The name of the project.
        """
        self.project_name = project_name
        self.test_runner = TestRunner(project_name)
        self.ai_interaction = AIInteraction()

    def improve_code(self):
        """
        Run tests and iteratively improve the code until all tests pass.
        """
        all_tests_passed = self.test_runner.run_tests()

        while not all_tests_passed:
            print("Starting another iteration to fix errors...")
            all_tests_passed = self.test_runner.run_tests()

        print("All tests passed. Code improvement process is complete.")
