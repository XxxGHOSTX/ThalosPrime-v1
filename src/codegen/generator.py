"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime is an original proprietary software system, including but not limited to
its source code, system architecture, internal logic descriptions, documentation,
interfaces, diagrams, and design materials.

Unauthorized reproduction, modification, distribution, public display, or use of
this software or its associated materials is strictly prohibited without the
express written permission of the copyright holder.

Thalos Prime™ is a proprietary system.
"""

"""
Deterministic Code Generation System

Input → deterministic output:
- No randomness
- Stateless or explicitly state-driven
- Designed to be testable without CIS
"""

from typing import Dict, Any, Optional


class CodeGenerator:
    """
    Deterministic Code Generator
    
    Principles:
    - Input → deterministic output
    - No randomness (no timestamps, UUIDs, etc.)
    - Stateless operation (history is optional explicit state)
    - Testable in isolation without CIS
    """
    
    def __init__(self, track_history: bool = False):
        """
        Initialize the Code Generator
        
        Args:
            track_history: Whether to maintain generation history (explicit state)
        """
        self.templates: Dict[str, str] = {}
        self.track_history = track_history
        self.generation_history: list = []
        
    def register_template(self, template_name: str, template_content: str) -> bool:
        """
        Register a code template
        
        Args:
            template_name: Unique identifier for the template
            template_content: Template content string
            
        Returns:
            bool: True if registration successful, False if already exists
        """
        if template_name in self.templates:
            return False
        self.templates[template_name] = template_content
        return True
        
    def generate(self, template_name: str, context: Dict[str, Any]) -> Optional[str]:
        """
        Generate code from a template with given context (deterministic)
        
        Args:
            template_name: Name of the template to use
            context: Dictionary of variables to substitute in template
            
        Returns:
            Generated code string if successful, None otherwise
        """
        if template_name not in self.templates:
            return None
            
        template = self.templates[template_name]
        
        # Deterministic template substitution
        try:
            generated_code = template.format(**context)
            
            # Optionally record generation history (explicit state)
            if self.track_history:
                self.generation_history.append({
                    'template': template_name,
                    'context_keys': sorted(context.keys())  # Sorted for determinism
                })
            
            return generated_code
        except KeyError:
            # Missing required context variable
            return None
            
    def generate_class(self, class_name: str, methods: list = None) -> str:
        """
        Generate a class structure deterministically
        
        Args:
            class_name: Name of the class to generate
            methods: Optional list of method names to include
            
        Returns:
            Generated class code
        """
        methods = methods or ['__init__']
        
        code_lines = [
            f'class {class_name}:',
            f'    """Auto-generated {class_name} class"""',
            ''
        ]
        
        for method in methods:
            if method == '__init__':
                code_lines.extend([
                    '    def __init__(self):',
                    f'        """Initialize {class_name}"""',
                    '        pass',
                    ''
                ])
            else:
                code_lines.extend([
                    f'    def {method}(self):',
                    f'        """Auto-generated {method} method"""',
                    '        pass',
                    ''
                ])
        
        return '\n'.join(code_lines)
        
    def generate_function(self, function_name: str, parameters: list = None) -> str:
        """
        Generate a function structure deterministically
        
        Args:
            function_name: Name of the function to generate
            parameters: Optional list of parameter names
            
        Returns:
            Generated function code
        """
        parameters = parameters or []
        param_str = ', '.join(parameters) if parameters else ''
        
        code_lines = [
            f'def {function_name}({param_str}):',
            f'    """Auto-generated {function_name} function"""',
            '    pass'
        ]
        
        return '\n'.join(code_lines)
        
    def list_templates(self) -> list:
        """
        List all registered templates (sorted for determinism)
        
        Returns:
            Sorted list of template names
        """
        return sorted(self.templates.keys())
        
    def get_history(self) -> list:
        """
        Get code generation history (if tracking enabled)
        
        Returns:
            List of generation records
        """
        return self.generation_history.copy()
        
    def clear_history(self) -> None:
        """Clear generation history"""
        self.generation_history.clear()
