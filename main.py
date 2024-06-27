from user_input import UserInput
from ai_interaction import AIInteraction
from code_generator import CodeGenerator
from iterative_improver import IterativeImprover

def main():
    # Get project details from the user
    project_details = UserInput.get_project_details()
    project_name = project_details['project_name']

    # Initialize AI Interaction and Code Generator
    ai_interaction = AIInteraction()
    code_generator = CodeGenerator(project_name)

    # Get module and function details, generate code, and save it
    while True:
        module_details = UserInput.get_module_details()
        class_name = module_details['module_name']
        class_description = module_details['module_description']
        class_code = ai_interaction.generate_class_code(class_name, class_description)
        code_generator.save_class_code(class_name, class_code)

        function_details = UserInput.get_function_details()
        function_name = function_details['function_name']
        function_description = function_details['function_description']
        function_code = ai_interaction.generate_function_code(function_name, function_description)
        code_generator.save_function_code(class_name, function_name, function_code)

        another_module = input("Do you want to add another module? (yes/no): ")
        if another_module.lower() != 'yes':
            break

    # Initialize IterativeImprover and start the improvement process
    iterative_improver = IterativeImprover(project_name)
    iterative_improver.improve_code()

if __name__ == "__main__":
    main()
