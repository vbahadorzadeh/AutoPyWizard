import openai
from gpt4all import GPT4All

class AIInteraction:
    """
    A class to handle interactions with AI models for code generation.
    Supports both gpt4all and OpenAI's API.
    """

    def __init__(self, use_openai=False, model_name='wizardcoder-33b-v1.1.Q4_0.gguf'):
        """
        Initialize the AIInteraction class with the specified model.
        
        Args:
            use_openai (bool): Flag to use OpenAI API instead of gpt4all.
            model_name (str): The name of the AI model to use.
        """
        self.use_openai = use_openai
        self.model_name = model_name
        if not self.use_openai:
            self.model = GPT4All(model=model_name)
        else:
            self.openai_api_key = None
            self.openai_base_url = None
            self.openai_model_name = model_name

    def set_openai_credentials(self, api_key, base_url):
        """
        Set the OpenAI API credentials.
        
        Args:
            api_key (str): The OpenAI API key.
            base_url (str): The base URL for the OpenAI API.
        """
        self.openai_api_key = api_key
        self.openai_base_url = base_url

    def get_openai_models(self):
        """
        Fetch available models from OpenAI API.
        
        Returns:
            list: A list of available OpenAI models.
        """
        openai.api_key = self.openai_api_key
        openai.api_base = self.openai_base_url
        models = openai.Model.list_models()
        return [model['id'] for model in models['data']]

    def generate_code(self, prompt):
        """
        Generate code using the specified AI model based on the provided prompt.
        
        Args:
            prompt (str): The prompt for the AI model.
        
        Returns:
            str: The generated code.
        """
        if self.use_openai:
            return self.generate_code_openai(prompt)
        else:
            return self.generate_code_gpt4all(prompt)

    def generate_code_gpt4all(self, prompt):
        """
        Generate code using the gpt4all model.
        
        Args:
            prompt (str): The prompt for the AI model.
        
        Returns:
            str: The generated code.
        """
        response = self.model.generate(prompt)
        return response

    def generate_code_openai(self, prompt):
        """
        Generate code using the OpenAI model.
        
        Args:
            prompt (str): The prompt for the AI model.
        
        Returns:
            str: The generated code.
        """
        openai.api_key = self.openai_api_key
        openai.api_base = self.openai_base_url
        
        response = openai.Completion.create(
            model=self.openai_model_name,
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()

    def generate_class_code(self, class_name, class_description):
        """
        Generate code for a class based on the class name and description.
        
        Args:
            class_name (str): The name of the class.
            class_description (str): The description of the class.
        
        Returns:
            str: The generated class code.
        """
        prompt = f"Generate a Python class named '{class_name}' with the following description: {class_description}"
        return self.generate_code(prompt)

    def generate_function_code(self, function_name, function_description):
        """
        Generate code for a function based on the function name and description.
        
        Args:
            function_name (str): The name of the function.
            function_description (str): The description of the function.
        
        Returns:
            str: The generated function code.
        """
        prompt = f"Generate a Python function named '{function_name}' with the following description: {function_description}"
        return self.generate_code(prompt)
