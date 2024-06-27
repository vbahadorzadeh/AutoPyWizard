class UserInput:
    """
    A class to handle user inputs for project and module details.
    """

    @staticmethod
    def get_project_details():
        """
        Get project name and description from the user.
        
        Returns:
            dict: A dictionary containing project name and description.
        """
        project_name = input("Enter the project name: ")
        project_description = input("Enter the project description: ")
        return {
            "project_name": project_name,
            "project_description": project_description
        }

    @staticmethod
    def get_module_details():
        """
        Get module name and description from the user.
        
        Returns:
            dict: A dictionary containing module name and description.
        """
        module_name = input("Enter the module name: ")
        module_description = input("Enter the module description: ")
        return {
            "module_name": module_name,
            "module_description": module_description
        }

    @staticmethod
    def get_function_details():
        """
        Get function name and description from the user.
        
        Returns:
            dict: A dictionary containing function name and description.
        """
        function_name = input("Enter the function name: ")
        function_description = input("Enter the function description: ")
        return {
            "function_name": function_name,
            "function_description": function_description
        }
