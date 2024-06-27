from flask import Flask, render_template, request, redirect, url_for, session
from ai_interaction import AIInteraction
from code_generator import CodeGenerator
from iterative_improver import IterativeImprover
from requirements_manager import RequirementsManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use sessions

project_details = {}
modules = []
functions = []
ai_settings = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set-ai-settings', methods=['GET', 'POST'])
def set_ai_settings():
    global ai_settings
    if request.method == 'POST':
        ai_provider = request.form['ai_provider']
        model_name = request.form['model_name']
        ai_settings = {
            'ai_provider': ai_provider,
            'model_name': model_name
        }
        if ai_provider == 'openai':
            ai_settings['api_key'] = request.form['api_key']
            ai_settings['base_url'] = request.form['base_url']
            session['api_key'] = request.form['api_key']
            session['base_url'] = request.form['base_url']
            return redirect(url_for('openai_models'))
        else:
            return redirect(url_for('project'))
    return render_template('ai_settings.html')

@app.route('/openai-models', methods=['GET', 'POST'])
def openai_models():
    if request.method == 'POST':
        ai_settings['model_name'] = request.form['model_name']
        return redirect(url_for('project'))
    
    ai_interaction = AIInteraction(use_openai=True)
    ai_interaction.set_openai_credentials(api_key=session['api_key'], base_url=session['base_url'])
    models = ai_interaction.get_openai_models()
    return render_template('openai_models.html', models=models)

@app.route('/project', methods=['GET', 'POST'])
def project():
    global project_details
    if request.method == 'POST':
        project_details = {
            'project_name': request.form['project_name'],
            'project_description': request.form['project_description']
        }
        if 'generate_modules' in request.form:
            return redirect(url_for('generate_modules'))
        return redirect(url_for('module'))
    return render_template('project.html')

@app.route('/generate_modules', methods=['GET', 'POST'])
def generate_modules():
    ai_interaction = AIInteraction(
        use_openai=ai_settings['ai_provider'] == 'openai',
        model_name=ai_settings['model_name']
    )
    if ai_settings['ai_provider'] == 'openai':
        ai_interaction.set_openai_credentials(
            api_key=ai_settings['api_key'],
            base_url=ai_settings['base_url']
        )
    
    prompt = f"Generate a list of modules with names and descriptions for a project with the following description: {project_details['project_description']}"
    response = ai_interaction.generate_code(prompt)
    
    generated_modules = parse_generated_modules(response)  # Assume a function to parse the response into a list of modules
    return render_template('generated_modules.html', modules=generated_modules)

@app.route('/module', methods=['GET', 'POST'])
def module():
    if request.method == 'POST':
        module_details = {
            'module_name': request.form['module_name'],
            'module_description': request.form['module_description']
        }
        modules.append(module_details)
        return redirect(url_for('function', module_name=module_details['module_name']))
    return render_template('module.html')

@app.route('/function/<module_name>', methods=['GET', 'POST'])
def function(module_name):
    if request.method == 'POST':
        function_details = {
            'function_name': request.form['function_name'],
            'function_description': request.form['function_description']
        }
        functions.append((module_name, function_details))
        if 'add_more' in request.form:
            return redirect(url_for('function', module_name=module_name))
        else:
            return redirect(url_for('module'))
    return render_template('function.html', module_name=module_name)

@app.route('/requirements', methods=['GET', 'POST'])
def requirements():
    if request.method == 'POST':
        packages = request.form['packages'].split()
        requirements_manager = RequirementsManager(project_details['project_name'])
        for package in packages:
            requirements_manager.add_requirement(package)
        requirements_manager.install_requirements()
        return redirect(url_for('progress'))
    return render_template('requirements.html')

@app.route('/progress')
def progress():
    if ai_settings['ai_provider'] == 'openai':
        ai_interaction = AIInteraction(use_openai=True, model_name=ai_settings['model_name'])
        ai_interaction.set_openai_credentials(
            api_key=ai_settings['api_key'],
            base_url=ai_settings['base_url'],
        )
    else:
        ai_interaction = AIInteraction(use_openai=False, model_name=ai_settings['model_name'])

    code_generator = CodeGenerator(project_details['project_name'])

    for module in modules:
        class_code = ai_interaction.generate_class_code(module['module_name'], module['module_description'])
        code_generator.save_class_code(module['module_name'], class_code)

    for module_name, function in functions:
        function_code = ai_interaction.generate_function_code(function['function_name'], function['function_description'])
        code_generator.save_function_code(module_name, function['function_name'], function_code)

    iterative_improver = IterativeImprover(project_details['project_name'])
    iterative_improver.improve_code()

    return render_template('progress.html')

def parse_generated_modules(response):
    # Implement parsing logic to convert the response into a list of module names and descriptions
    modules = []
    lines = response.split('\n')
    for line in lines:
        if ':' in line:
            module_name, module_description = line.split(':', 1)
            modules.append({
                'module_name': module_name.strip(),
                'module_description': module_description.strip()
            })
    return modules

if __name__ == '__main__':
    app.run(debug=True)
