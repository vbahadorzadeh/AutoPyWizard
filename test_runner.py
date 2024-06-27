import unittest
import os
import traceback
from ai_interaction import AIInteraction
from code_generator import CodeGenerator

class TestRunner:
    """
    A class to handle running tests and managing exceptions for the generated code.
    """

    def __init__(self, project_name):
        """
        Initialize the TestRunner with the project name.
        
        Args:
            project_name (str): The name of the project.
        """
        self.project_name = project_name
        self.test_dir = os.path.join(os.getcwd(), project_name)
        self.ai_interaction = AIInteraction()

    def run_tests(self):
        """
        Run tests on the generated code.
        
        Returns:
            bool: True if all tests pass, False otherwise.
        """
        loader = unittest.TestLoader()
        suite = loader.discover(self.test_dir)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("All tests passed!")
            return True
        else:
            print("Some tests failed. Check the errors and revise the code.")
            for error in result.errors:
                self.handle_exceptions(error)
            for failure in result.failures:
                self.handle_exceptions(failure)
            return False

    def handle_exceptions(self, test_result):
        """
        Handle exceptions by sending the traceback to the AI for fixes.
        
        Args:
            test_result (tuple): The test case and the traceback information.
        """
        test_case, tb_info = test_result
        tb = ''.join(traceback.format_exception(None, tb_info, tb_info.__traceback__))
        prompt = f"Fix the following error in the code:\n{tb}"
        fixed_code = self.ai_interaction.generate_code(prompt)

        # Save the fixed code
        file_name = self.extract_file_name(tb)
        module_name = os.path.splitext(file_name)[0]
        CodeGenerator(self.project_name).save_function_code(module_name, "fixed_function", fixed_code)
        
        # Re-run the tests after fixing
        self.run_tests()

    def extract_file_name(self, traceback_info):
        """
        Extract the file name from the traceback information.
        
        Args:
            traceback_info (str): The traceback information.
        
        Returns:
            str: The name of the file where the error occurred.
        """
        lines = traceback_info.split('\n')
        for line in lines:
            if ".py" in line:
                return line.split('"')[1]
        return "unknown_file.py"
