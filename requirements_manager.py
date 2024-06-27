import os
import subprocess

class RequirementsManager:
    """
    A class to handle the creation and installation of requirements.txt.
    """

    def __init__(self, project_name):
        self.project_name = project_name
        self.requirements_path = os.path.join(os.getcwd(), project_name, 'requirements.txt')

    def add_requirement(self, package_name):
        """
        Add a package to requirements.txt.
        
        Args:
            package_name (str): The name of the package to add.
        """
        with open(self.requirements_path, 'a',encoding="utf-8") as requirements_file:
            requirements_file.write(f"{package_name}\n")
        print(f"Added {package_name} to requirements.txt")

    def install_requirements(self):
        """
        Install the packages listed in requirements.txt.
        """
        subprocess.run(['pip', 'install', '-r', self.requirements_path])
