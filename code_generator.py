import os

class CodeGenerator:
    """
    A class to handle saving generated code to files within a project directory.
    """

    def __init__(self, project_name):
        """
        Initialize the CodeGenerator with the project name.
        
        Args:
            project_name (str): The name of the project.
        """
        self.project_name = project_name
        self.project_dir = os.path.join(os.getcwd(), project_name)
        self.create_project_directory()

    def create_project_directory(self):
        """
        Create the main project directory if it does not exist.
        """
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)
            print(f"Project directory '{self.project_dir}' created.")
        else:
            print(f"Project directory '{self.project_dir}' already exists.")

    def save_code_to_file(self, file_name, code):
        """
        Save the generated code to a file within the project directory.
        
        Args:
            file_name (str): The name of the file to save the code.
            code (str): The generated code.
        """
        file_path = os.path.join(self.project_dir, file_name)
        with open(file_path, 'w') as file:
            file.write(code)
        print(f"Code saved to '{file_path}'.")

    def save_class_code(self, class_name, code):
        """
        Save the generated class code to a file within the project directory.
        
        Args:
            class_name (str): The name of the class.
            code (str): The generated class code.
        """
        file_name = f"{class_name.lower()}.py"
        self.save_code_to_file(file_name, code)

    def save_function_code(self, module_name, function_name, code):
        """
        Save the generated function code to a module file within the project directory.
        If the module file already exists, append the function code to the file.
        
        Args:
            module_name (str): The name of the module (file).
            function_name (str): The name of the function.
            code (str): The generated function code.
        """
        file_name = f"{module_name.lower()}.py"
        file_path = os.path.join(self.project_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'a') as file:
                file.write("\n\n" + code)
            print(f"Function '{function_name}' appended to '{file_path}'.")
        else:
            self.save_code_to_file(file_name, code)
