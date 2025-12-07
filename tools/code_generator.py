"""
Advanced Python Code Generator
Generates complete, production-ready Python code
"""
import ast
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import textwrap


class CodeTemplate:
    """Templates for common code patterns."""
    
    FUNCTION = '''def {name}({params}){returns}:
    """
    {docstring}
    
    Args:
{args_doc}
    
    Returns:
        {return_doc}
    """
{body}'''
    
    CLASS = '''class {name}{inheritance}:
    """
    {docstring}
    
    Attributes:
{attrs_doc}
    """
    
    def __init__(self{init_params}):
        """Initialize {name}."""
{init_body}
{methods}'''
    
    ASYNC_FUNCTION = '''async def {name}({params}){returns}:
    """
    {docstring}
    
    Args:
{args_doc}
    
    Returns:
        {return_doc}
    """
{body}'''
    
    DECORATOR = '''def {name}(func):
    """
    {docstring}
    """
    def wrapper(*args, **kwargs):
{body}
        return func(*args, **kwargs)
    return wrapper'''
    
    PROPERTY = '''    @property
    def {name}(self){returns}:
        """{docstring}"""
{body}
    
    @{name}.setter
    def {name}(self, value):
        """{setter_doc}"""
{setter_body}'''
    
    CONTEXT_MANAGER = '''class {name}:
    """
    {docstring}
    
    Usage:
        with {name}() as obj:
            # Use obj
    """
    
    def __enter__(self):
{enter_body}
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
{exit_body}
        return False'''
    
    DATACLASS = '''from dataclasses import dataclass, field
from typing import {types}

@dataclass
class {name}:
    """
    {docstring}
    """
{fields}'''
    
    API_CLIENT = '''import requests
from typing import Dict, Optional, Any

class {name}:
    """
    {docstring}
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({{'Authorization': f'Bearer {{api_key}}'}})
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request."""
        url = f"{{self.base_url}}/{{endpoint.lstrip('/')}}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """GET request."""
        return self._request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """POST request."""
        return self._request('POST', endpoint, json=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """PUT request."""
        return self._request('PUT', endpoint, json=data)
    
    def delete(self, endpoint: str) -> Dict:
        """DELETE request."""
        return self._request('DELETE', endpoint)'''
    
    CLI_APP = '''import argparse
import sys
from typing import List, Optional

def main(args: Optional[List[str]] = None) -> int:
    """
    {docstring}
    
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description='{description}',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
{arguments}
    
    parsed_args = parser.parse_args(args)
    
    try:
{main_logic}
        return 0
    except Exception as e:
        print(f"Error: {{e}}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())'''
    
    TEST_CLASS = '''import unittest
from unittest.mock import Mock, patch, MagicMock

class Test{class_name}(unittest.TestCase):
    """
    Tests for {class_name}
    """
    
    def setUp(self):
        """Set up test fixtures."""
{setup}
    
    def tearDown(self):
        """Clean up after tests."""
{teardown}
{test_methods}
    
if __name__ == '__main__':
    unittest.main()'''


class CodeGenerator:
    """Advanced Python code generator."""
    
    def __init__(self):
        self.indent = "    "
        self.generated_code = []
    
    def generate_function(self, name: str, params: List[Dict],
                         return_type: Optional[str] = None,
                         docstring: str = "",
                         body: str = "pass",
                         is_async: bool = False,
                         decorators: Optional[List[str]] = None) -> str:
        """
        Generate function code.
        
        Args:
            name: Function name
            params: List of {'name': str, 'type': str, 'default': Any}
            return_type: Return type annotation
            docstring: Function docstring
            body: Function body code
            is_async: Whether function is async
            decorators: List of decorator strings (e.g., ['@property', '@staticmethod'])
        """
        # Build decorators
        decorator_lines = []
        if decorators:
            for decorator in decorators:
                if not decorator.startswith('@'):
                    decorator = f'@{decorator}'
                decorator_lines.append(decorator)
        
        # Build parameter string
        param_strs = []
        for param in params:
            param_str = param['name']
            if 'type' in param:
                param_str += f": {param['type']}"
            if 'default' in param:
                default = param['default']
                if isinstance(default, str):
                    default = f"'{default}'"
                param_str += f" = {default}"
            param_strs.append(param_str)
        
        params_str = ", ".join(param_strs)
        
        # Build return annotation
        returns = f" -> {return_type}" if return_type else ""
        
        # Build args documentation
        args_doc = ""
        if params:
            args_lines = []
            for param in params:
                param_type = param.get('type', 'Any')
                param_desc = param.get('description', '')
                args_lines.append(f"        {param['name']} ({param_type}): {param_desc}")
            args_doc = "\n".join(args_lines)
        else:
            args_doc = "        None"
        
        # Build return documentation
        return_doc = return_type if return_type else "None"
        
        # Indent body
        body_lines = body.strip().split('\n')
        body_indented = '\n'.join(f"    {line}" if line else "" for line in body_lines)
        
        # Build decorators
        decorators_str = ""
        if decorators:
            decorator_lines = []
            for decorator in decorators:
                if not decorator.startswith('@'):
                    decorator = f'@{decorator}'
                decorator_lines.append(decorator)
            decorators_str = '\n'.join(decorator_lines) + '\n'
        
        # Choose template
        template = CodeTemplate.ASYNC_FUNCTION if is_async else CodeTemplate.FUNCTION
        
        code = template.format(
            name=name,
            params=params_str,
            returns=returns,
            docstring=docstring,
            args_doc=args_doc,
            return_doc=return_doc,
            body=body_indented
        )
        
        # Prepend decorators if any
        if decorators_str:
            code = decorators_str + code
        
        return code
    
    def generate_class(self, name: str, 
                      attributes: List[Dict],
                      methods: List[Dict],
                      inheritance: Optional[List[str]] = None,
                      docstring: str = "") -> str:
        """
        Generate class code.
        
        Args:
            name: Class name
            attributes: List of {'name': str, 'type': str, 'description': str}
            methods: List of method definitions
            inheritance: Parent classes
            docstring: Class docstring
        """
        # Build inheritance
        if inheritance:
            inherit_str = f"({', '.join(inheritance)})"
        else:
            inherit_str = ""
        
        # Build attributes documentation
        if attributes:
            attrs_lines = []
            for attr in attributes:
                attr_type = attr.get('type', 'Any')
                attr_desc = attr.get('description', '')
                attrs_lines.append(f"        {attr['name']} ({attr_type}): {attr_desc}")
            attrs_doc = "\n".join(attrs_lines)
        else:
            attrs_doc = "        None"
        
        # Build __init__ parameters
        init_params = ""
        init_body = ""
        if attributes:
            init_param_strs = []
            init_body_lines = []
            for attr in attributes:
                param_str = f", {attr['name']}"
                if 'type' in attr:
                    param_str += f": {attr['type']}"
                if 'default' in attr:
                    default = attr['default']
                    if isinstance(default, str):
                        default = f"'{default}'"
                    param_str += f" = {default}"
                init_param_strs.append(param_str)
                init_body_lines.append(f"        self.{attr['name']} = {attr['name']}")
            
            init_params = "".join(init_param_strs)
            init_body = "\n".join(init_body_lines)
        else:
            init_body = "        pass"
        
        # Build methods
        methods_code = ""
        if methods:
            method_strs = []
            for method in methods:
                method_code = self.generate_function(
                    name=method['name'],
                    params=[{'name': 'self', 'type': ''}] + method.get('params', []),
                    return_type=method.get('return_type'),
                    docstring=method.get('docstring', ''),
                    body=method.get('body', 'pass'),
                    is_async=method.get('is_async', False)
                )
                # Add indentation for class method
                method_lines = method_code.split('\n')
                method_indented = '\n'.join(f"    {line}" if line else "" for line in method_lines)
                method_strs.append(method_indented)
            
            methods_code = "\n\n".join(method_strs)
        
        code = CodeTemplate.CLASS.format(
            name=name,
            inheritance=inherit_str,
            docstring=docstring,
            attrs_doc=attrs_doc,
            init_params=init_params,
            init_body=init_body,
            methods="\n\n" + methods_code if methods_code else ""
        )
        
        return code
    
    def generate_dataclass(self, name: str, fields: List[Dict],
                          docstring: str = "") -> str:
        """
        Generate dataclass code.
        
        Args:
            name: Dataclass name
            fields: List of {'name': str, 'type': str, 'default': Any}
            docstring: Class docstring
        """
        # Collect unique types
        types = set()
        for field in fields:
            field_type = field.get('type', 'Any')
            types.add(field_type)
        
        types_str = ", ".join(sorted(types))
        
        # Build fields
        field_lines = []
        for field in fields:
            field_str = f"    {field['name']}: {field.get('type', 'Any')}"
            if 'default' in field:
                default = field['default']
                if isinstance(default, str):
                    default = f"'{default}'"
                elif default is None:
                    default = "None"
                field_str += f" = {default}"
            elif 'default_factory' in field:
                field_str += f" = field(default_factory={field['default_factory']})"
            field_lines.append(field_str)
        
        fields_str = "\n".join(field_lines)
        
        code = CodeTemplate.DATACLASS.format(
            types=types_str or "Any",
            name=name,
            docstring=docstring,
            fields=fields_str
        )
        
        return code
    
    def generate_decorator(self, name: str, docstring: str = "",
                          body: str = "") -> str:
        """Generate decorator code."""
        if not body:
            body = "        # Add custom logic here\n        pass"
        
        body_lines = body.strip().split('\n')
        body_indented = '\n'.join(f"        {line}" if line else "" for line in body_lines)
        
        code = CodeTemplate.DECORATOR.format(
            name=name,
            docstring=docstring,
            body=body_indented
        )
        
        return code
    
    def generate_property(self, name: str, return_type: Optional[str] = None,
                         getter_body: str = "", setter_body: str = "",
                         docstring: str = "",
                         setter_doc: str = "") -> str:
        """Generate property with getter and setter."""
        returns = f" -> {return_type}" if return_type else ""
        
        getter_lines = (getter_body or f"return self._{name}").strip().split('\n')
        getter_indented = '\n'.join(f"        {line}" if line else "" for line in getter_lines)
        
        setter_lines = (setter_body or f"self._{name} = value").strip().split('\n')
        setter_indented = '\n'.join(f"        {line}" if line else "" for line in setter_lines)
        
        code = CodeTemplate.PROPERTY.format(
            name=name,
            returns=returns,
            docstring=docstring,
            body=getter_indented,
            setter_doc=setter_doc or f"Set {name}.",
            setter_body=setter_indented
        )
        
        return code
    
    def generate_context_manager(self, name: str, docstring: str = "",
                                enter_body: str = "", exit_body: str = "") -> str:
        """Generate context manager class."""
        enter_lines = (enter_body or "pass").strip().split('\n')
        enter_indented = '\n'.join(f"        {line}" if line else "" for line in enter_lines)
        
        exit_lines = (exit_body or "pass").strip().split('\n')
        exit_indented = '\n'.join(f"        {line}" if line else "" for line in exit_lines)
        
        code = CodeTemplate.CONTEXT_MANAGER.format(
            name=name,
            docstring=docstring,
            enter_body=enter_indented,
            exit_body=exit_indented
        )
        
        return code
    
    def generate_api_client(self, name: str, docstring: str = "") -> str:
        """Generate REST API client class."""
        code = CodeTemplate.API_CLIENT.format(
            name=name,
            docstring=docstring or f"REST API client for {name}."
        )
        
        return code
    
    def generate_cli_app(self, name: str, description: str,
                        arguments: List[Dict],
                        main_logic: str = "") -> str:
        """
        Generate CLI application.
        
        Args:
            name: App name
            description: App description
            arguments: List of {'name': str, 'type': str, 'help': str, 'required': bool}
            main_logic: Main logic code
        """
        # Build arguments
        arg_lines = []
        for arg in arguments:
            if arg.get('positional'):
                arg_str = f"    parser.add_argument('{arg['name']}'"
            else:
                arg_str = f"    parser.add_argument('--{arg['name']}'"
            
            if 'type' in arg:
                arg_str += f", type={arg['type']}"
            if 'help' in arg:
                arg_str += f", help='{arg['help']}'"
            if arg.get('required'):
                arg_str += ", required=True"
            if 'default' in arg:
                default = arg['default']
                if isinstance(default, str):
                    default = f"'{default}'"
                arg_str += f", default={default}"
            
            arg_str += ")"
            arg_lines.append(arg_str)
        
        arguments_str = "\n".join(arg_lines)
        
        # Build main logic
        if not main_logic:
            logic_lines = ["        # Add your logic here"]
            for arg in arguments:
                arg_name = arg['name']
                logic_lines.append(f"        print(f'{{parsed_args.{arg_name}}}')")
            main_logic = "\n".join(logic_lines)
        else:
            logic_lines = main_logic.strip().split('\n')
            main_logic = '\n'.join(f"        {line}" if line else "" for line in logic_lines)
        
        code = CodeTemplate.CLI_APP.format(
            docstring=description,
            description=description,
            arguments=arguments_str,
            main_logic=main_logic
        )
        
        return code
    
    def generate_test_class(self, class_name: str,
                           test_methods: List[Dict],
                           setup: str = "",
                           teardown: str = "") -> str:
        """
        Generate test class.
        
        Args:
            class_name: Class being tested
            test_methods: List of {'name': str, 'body': str}
            setup: Setup code
            teardown: Teardown code
        """
        # Build setup
        setup_lines = (setup or "pass").strip().split('\n')
        setup_str = '\n'.join(f"        {line}" if line else "" for line in setup_lines)
        
        # Build teardown
        teardown_lines = (teardown or "pass").strip().split('\n')
        teardown_str = '\n'.join(f"        {line}" if line else "" for line in teardown_lines)
        
        # Build test methods
        test_strs = []
        for test in test_methods:
            test_name = test['name']
            if not test_name.startswith('test_'):
                test_name = f"test_{test_name}"
            
            test_body = test.get('body', 'self.assertTrue(True)')
            test_body_lines = test_body.strip().split('\n')
            test_body_str = '\n'.join(f"        {line}" if line else "" for line in test_body_lines)
            
            test_code = f'''    def {test_name}(self):
        """{test.get('docstring', f'Test {test_name}')}"""
{test_body_str}'''
            test_strs.append(test_code)
        
        tests_str = "\n\n".join(test_strs)
        
        code = CodeTemplate.TEST_CLASS.format(
            class_name=class_name,
            setup=setup_str,
            teardown=teardown_str,
            test_methods="\n\n" + tests_str if tests_str else ""
        )
        
        return code
    
    def generate_script(self, name: str, imports: List[str],
                       functions: List[str], main_code: str = "") -> str:
        """
        Generate complete Python script.
        
        Args:
            name: Script name/description
            imports: List of import statements
            functions: List of function code strings
            main_code: Main execution code
        """
        script_parts = []
        
        # Header comment
        script_parts.append(f'''"""
{name}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""''')
        
        # Imports
        if imports:
            script_parts.append("\n".join(imports))
        
        # Functions
        if functions:
            script_parts.extend(functions)
        
        # Main code
        if main_code:
            script_parts.append("\n\nif __name__ == '__main__':")
            main_lines = main_code.strip().split('\n')
            main_indented = '\n'.join(f"    {line}" if line else "" for line in main_lines)
            script_parts.append(main_indented)
        
        return "\n\n".join(script_parts)
    
    def validate_code(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Python code syntax.
        
        Returns:
            (is_valid, error_message)
        """
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)
    
    def format_code(self, code: str) -> str:
        """Format code with proper indentation."""
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Decrease indent for closing brackets
            if stripped.startswith((')', ']', '}')):
                indent_level = max(0, indent_level - 1)
            
            # Decrease indent for else, elif, except, finally
            if re.match(r'^(else|elif|except|finally):', stripped):
                indent_level = max(0, indent_level - 1)
            
            # Add line with proper indentation
            if stripped:
                formatted_lines.append(self.indent * indent_level + stripped)
            else:
                formatted_lines.append("")
            
            # Increase indent after colons
            if stripped.endswith(':'):
                indent_level += 1
            
            # Increase indent for opening brackets
            if stripped.endswith(('(', '[', '{')):
                indent_level += 1
        
        return '\n'.join(formatted_lines)
    
    def generate_from_description(self, description: str) -> str:
        """
        Generate code from natural language description.
        
        This is a simple pattern matcher - for complex generation,
        integrate with LLM.
        """
        description_lower = description.lower()
        
        # Detect patterns
        if 'function' in description_lower or 'def ' in description_lower:
            # Extract function name
            match = re.search(r'(?:function|def)\s+(\w+)', description_lower)
            if match:
                func_name = match.group(1)
                return self.generate_function(
                    name=func_name,
                    params=[],
                    docstring=description,
                    body="# TODO: Implement function logic\npass"
                )
        
        elif 'class' in description_lower:
            # Extract class name
            match = re.search(r'class\s+(\w+)', description_lower)
            if match:
                class_name = match.group(1)
                return self.generate_class(
                    name=class_name,
                    attributes=[],
                    methods=[],
                    docstring=description
                )
        
        elif 'api' in description_lower or 'rest' in description_lower:
            # Generate API client
            match = re.search(r'(\w+)\s+api', description_lower)
            if match:
                api_name = match.group(1).title() + "API"
                return self.generate_api_client(api_name, description)
        
        elif 'cli' in description_lower or 'command line' in description_lower:
            # Generate CLI app
            return self.generate_cli_app(
                name="CLIApp",
                description=description,
                arguments=[
                    {'name': 'input', 'positional': True, 'help': 'Input file'}
                ]
            )
        
        # Default: generate a simple function
        return self.generate_function(
            name="generated_function",
            params=[],
            docstring=description,
            body="# TODO: Implement logic\npass"
        )


# Global instance
_generator = CodeGenerator()

def generate_function(name: str, params: List[Dict], **kwargs) -> str:
    """Generate function code."""
    return _generator.generate_function(name, params, **kwargs)

def generate_class(name: str, attributes: List[Dict], methods: List[Dict], **kwargs) -> str:
    """Generate class code."""
    return _generator.generate_class(name, attributes, methods, **kwargs)

def validate_code(code: str) -> Tuple[bool, Optional[str]]:
    """Validate Python code."""
    return _generator.validate_code(code)
