"""
PowerShell Advanced Generator
Sistema avanzato per generazione, analisi e gestione script PowerShell
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from jinja2 import Template, Environment, FileSystemLoader
import pyparsing as pp
from collections import defaultdict


class PowerShellScriptGenerator:
    """Generatore avanzato di script PowerShell"""
    
    def __init__(self):
        """Inizializza il generatore"""
        self.indent = "    "
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, str]:
        """Carica template PowerShell predefiniti"""
        return {
            'function': '''function {{ name }} {
    <#
    .SYNOPSIS
        {{ synopsis }}
    
    .DESCRIPTION
        {{ description }}
    
    .PARAMETER {{ param_name }}
        {{ param_desc }}
    
    .EXAMPLE
        {{ example }}
    #>
    
    [CmdletBinding()]
    param(
        {% for param in parameters %}
        [{{ param.type }}]${{ param.name }}{% if param.mandatory %}[Parameter(Mandatory=$true)]{% endif %}{% if not loop.last %},{% endif %}
        {% endfor %}
    )
    
    begin {
        Write-Verbose "Starting {{ name }}"
    }
    
    process {
        {{ body }}
    }
    
    end {
        Write-Verbose "Completed {{ name }}"
    }
}''',
            
            'cmdlet': '''function {{ verb }}-{{ noun }} {
    <#
    .SYNOPSIS
        {{ synopsis }}
    
    .DESCRIPTION
        {{ description }}
    
    .NOTES
        Name: {{ verb }}-{{ noun }}
        Author: Super Agent
        Version: 1.0
        DateCreated: {{ date }}
    #>
    
    [CmdletBinding(SupportsShouldProcess=$true)]
    param(
        {% for param in parameters %}
        [Parameter({% if param.mandatory %}Mandatory=$true, {% endif %}{% if param.pipeline %}ValueFromPipeline=$true, {% endif %}Position={{ loop.index0 }})]
        [{{ param.type }}]
        ${{ param.name }}{% if param.default %} = {{ param.default }}{% endif %}{% if not loop.last %},{% endif %}
        {% endfor %}
    )
    
    begin {
        Write-Verbose "[$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))] Starting {{ verb }}-{{ noun }}"
        {{ begin_block }}
    }
    
    process {
        if ($PSCmdlet.ShouldProcess("${{ target_param }}", "{{ verb }}")) {
            try {
                {{ process_block }}
            }
            catch {
                Write-Error "Error in {{ verb }}-{{ noun }}: $_"
                throw
            }
        }
    }
    
    end {
        Write-Verbose "[$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))] Completed {{ verb }}-{{ noun }}"
        {{ end_block }}
    }
}''',
            
            'module': '''<#
.SYNOPSIS
    {{ module_name }} - {{ synopsis }}

.DESCRIPTION
    {{ description }}

.NOTES
    Name: {{ module_name }}
    Author: Super Agent
    Version: {{ version }}
    DateCreated: {{ date }}
#>

# Module variables
$Script:ModuleName = "{{ module_name }}"
$Script:ModuleVersion = "{{ version }}"

# Export module members
Export-ModuleMember -Function @(
    {% for func in functions %}
    '{{ func }}'{% if not loop.last %},{% endif %}
    {% endfor %}
)

{{ content }}
''',
            
            'class': '''class {{ name }} {
    # Properties
    {% for prop in properties %}
    [{{ prop.type }}]${{ prop.name }}
    {% endfor %}
    
    # Constructor
    {{ name }}({% for prop in properties %}[{{ prop.type }}]${{ prop.name }}{% if not loop.last %}, {% endif %}{% endfor %}) {
        {% for prop in properties %}
        $this.{{ prop.name }} = ${{ prop.name }}
        {% endfor %}
    }
    
    # Methods
    {% for method in methods %}
    [{{ method.return_type }}]{{ method.name }}({% for param in method.parameters %}[{{ param.type }}]${{ param.name }}{% if not loop.last %}, {% endif %}{% endfor %}) {
        {{ method.body }}
    }
    {% endfor %}
}''',
            
            'script_header': '''<#
.SYNOPSIS
    {{ title }}

.DESCRIPTION
    {{ description }}

.PARAMETER {{ param_name }}
    {{ param_desc }}

.EXAMPLE
    {{ example }}

.NOTES
    Name: {{ script_name }}
    Author: {{ author }}
    Version: {{ version }}
    DateCreated: {{ date }}
    
.LINK
    {{ link }}
#>

[CmdletBinding()]
param(
    {% for param in parameters %}
    [Parameter({% if param.mandatory %}Mandatory=$true, {% endif %}Position={{ loop.index0 }})]
    [{{ param.type }}]
    ${{ param.name }}{% if param.default %} = {{ param.default }}{% endif %}{% if not loop.last %},{% endif %}
    {% endfor %}
)

# Script configuration
$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

# Logging
$LogFile = "{{ log_file }}"
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp] [$Level] $Message"
    Write-Verbose $LogMessage
    Add-Content -Path $LogFile -Value $LogMessage
}

Write-Log "Starting {{ script_name }}"

# Main script logic
try {
    {{ main_logic }}
}
catch {
    Write-Log "Error: $_" -Level "ERROR"
    throw
}
finally {
    Write-Log "Completed {{ script_name }}"
}
''',
            
            'error_handling': '''try {
    {{ try_block }}
}
catch [System.{{ exception_type }}] {
    Write-Error "{{ exception_type }}: $_"
    {{ catch_block }}
}
catch {
    Write-Error "Unexpected error: $_"
    throw
}
finally {
    {{ finally_block }}
}''',
            
            'pipeline': '''{{ input }} |
    {% for stage in stages %}
    {{ stage.cmdlet }} {{ stage.parameters }}{% if stage.script_block %} { {{ stage.script_block }} }{% endif %}{% if not loop.last %} |{% endif %}
    {% endfor %}''',
        }
    
    def generate_function(self, name: str, parameters: List[Dict], 
                         synopsis: str, body: str, 
                         description: str = "", example: str = "") -> str:
        """
        Genera una funzione PowerShell avanzata
        
        Args:
            name: Nome funzione
            parameters: Lista parametri con type, name, mandatory
            synopsis: Breve descrizione
            body: Corpo della funzione
            description: Descrizione estesa
            example: Esempio utilizzo
        """
        template = Template(self.templates['function'])
        
        return template.render(
            name=name,
            synopsis=synopsis,
            description=description or synopsis,
            param_name=parameters[0]['name'] if parameters else 'Parameter',
            param_desc=parameters[0].get('description', 'Parameter description') if parameters else 'N/A',
            example=example or f"{name} -Parameter Value",
            parameters=parameters,
            body=body
        )
    
    def generate_cmdlet(self, verb: str, noun: str,
                       parameters: List[Dict],
                       synopsis: str,
                       process_block: str,
                       begin_block: str = "",
                       end_block: str = "",
                       description: str = "",
                       target_param: str = None) -> str:
        """
        Genera un cmdlet PowerShell completo con best practices
        
        Args:
            verb: Verb approvato (Get, Set, New, Remove, etc)
            noun: Noun descrittivo
            parameters: Lista parametri
            synopsis: Descrizione breve
            process_block: Codice process block
            begin_block: Codice begin block (opzionale)
            end_block: Codice end block (opzionale)
            description: Descrizione estesa
            target_param: Parametro target per ShouldProcess
        """
        template = Template(self.templates['cmdlet'])
        
        if not target_param and parameters:
            target_param = parameters[0]['name']
        
        return template.render(
            verb=verb,
            noun=noun,
            synopsis=synopsis,
            description=description or synopsis,
            date=datetime.now().strftime('%Y-%m-%d'),
            parameters=parameters,
            begin_block=begin_block or "# Initialization",
            process_block=process_block,
            end_block=end_block or "# Cleanup",
            target_param=target_param or "Target"
        )
    
    def generate_class(self, name: str, 
                      properties: List[Dict],
                      methods: List[Dict]) -> str:
        """
        Genera una classe PowerShell
        
        Args:
            name: Nome classe
            properties: Lista proprietà con type e name
            methods: Lista metodi con name, return_type, parameters, body
        """
        template = Template(self.templates['class'])
        
        return template.render(
            name=name,
            properties=properties,
            methods=methods
        )
    
    def generate_module(self, module_name: str,
                       functions: List[str],
                       content: str,
                       synopsis: str = "",
                       description: str = "",
                       version: str = "1.0.0") -> str:
        """
        Genera un modulo PowerShell completo
        
        Args:
            module_name: Nome modulo
            functions: Lista nomi funzioni da esportare
            content: Contenuto del modulo (funzioni, classi, etc)
            synopsis: Descrizione breve
            description: Descrizione estesa
            version: Versione modulo
        """
        template = Template(self.templates['module'])
        
        return template.render(
            module_name=module_name,
            synopsis=synopsis or f"{module_name} PowerShell Module",
            description=description or synopsis or f"{module_name} PowerShell Module",
            version=version,
            date=datetime.now().strftime('%Y-%m-%d'),
            functions=functions,
            content=content
        )
    
    def generate_script_with_header(self, title: str,
                                   parameters: List[Dict],
                                   main_logic: str,
                                   description: str = "",
                                   author: str = "Super Agent",
                                   version: str = "1.0",
                                   log_file: str = "script.log",
                                   link: str = "") -> str:
        """
        Genera uno script completo con header e logging
        
        Args:
            title: Titolo script
            parameters: Lista parametri
            main_logic: Logica principale
            description: Descrizione
            author: Autore
            version: Versione
            log_file: Path file log
            link: Link documentazione
        """
        template = Template(self.templates['script_header'])
        
        script_name = title.replace(' ', '')
        
        return template.render(
            title=title,
            description=description or title,
            param_name=parameters[0]['name'] if parameters else 'Parameter',
            param_desc=parameters[0].get('description', 'Parameter description') if parameters else 'N/A',
            example=f".\\{script_name}.ps1 -Parameter Value",
            script_name=script_name,
            author=author,
            version=version,
            date=datetime.now().strftime('%Y-%m-%d'),
            link=link or "https://github.com/super-agent",
            parameters=parameters,
            log_file=log_file,
            main_logic=main_logic
        )
    
    def generate_error_handling(self, try_block: str,
                               catch_block: str = "",
                               finally_block: str = "",
                               exception_type: str = "Exception") -> str:
        """Genera blocco try-catch-finally"""
        template = Template(self.templates['error_handling'])
        
        return template.render(
            try_block=try_block,
            exception_type=exception_type,
            catch_block=catch_block or "# Handle error",
            finally_block=finally_block or "# Cleanup"
        )
    
    def generate_pipeline(self, input_cmd: str, stages: List[Dict]) -> str:
        """
        Genera una pipeline PowerShell
        
        Args:
            input_cmd: Comando iniziale
            stages: Lista stage con cmdlet, parameters, script_block
        """
        template = Template(self.templates['pipeline'])
        
        return template.render(
            input=input_cmd,
            stages=stages
        )
    
    def generate_advanced_function_from_spec(self, spec: Dict) -> str:
        """
        Genera funzione avanzata da specifica completa
        
        Args:
            spec: Dictionary con name, verb, noun, parameters, logic, etc
        """
        # Estrai componenti
        name = spec.get('name', 'New-Function')
        parameters = spec.get('parameters', [])
        synopsis = spec.get('synopsis', 'Function description')
        logic = spec.get('logic', '# Implementation here')
        
        # Genera validazione parametri
        validation = []
        for param in parameters:
            if param.get('validate'):
                val_type = param['validate'].get('type')
                if val_type == 'range':
                    min_val = param['validate'].get('min', 0)
                    max_val = param['validate'].get('max', 100)
                    validation.append(f"if (${param['name']} -lt {min_val} -or ${param['name']} -gt {max_val}) {{")
                    validation.append(f"    throw 'Parameter {param['name']} must be between {min_val} and {max_val}'")
                    validation.append("}")
                elif val_type == 'notnull':
                    validation.append(f"if ($null -eq ${param['name']}) {{")
                    validation.append(f"    throw 'Parameter {param['name']} cannot be null'")
                    validation.append("}")
        
        # Combina logica
        full_logic = "\n".join(validation) + "\n\n" + logic if validation else logic
        
        return self.generate_function(
            name=name,
            parameters=parameters,
            synopsis=synopsis,
            body=full_logic,
            description=spec.get('description', synopsis),
            example=spec.get('example', f"{name} -Parameter Value")
        )


class PowerShellAnalyzer:
    """Analizzatore avanzato di script PowerShell"""
    
    def __init__(self):
        """Inizializza l'analizzatore"""
        self.cmdlet_pattern = re.compile(r'\b([A-Z][a-z]+-[A-Z][a-z]+)\b')
        self.variable_pattern = re.compile(r'\$[A-Za-z_][A-Za-z0-9_]*')
        self.parameter_pattern = re.compile(r'-([A-Za-z]+)')
        self.comment_pattern = re.compile(r'#.*$', re.MULTILINE)
        
    def analyze_script(self, script: str) -> Dict[str, Any]:
        """
        Analizza uno script PowerShell completo
        
        Args:
            script: Contenuto script
            
        Returns:
            Dictionary con analisi completa
        """
        lines = script.split('\n')
        
        analysis = {
            'metrics': self._calculate_metrics(script, lines),
            'cmdlets': self._extract_cmdlets(script),
            'variables': self._extract_variables(script),
            'parameters': self._extract_parameters(script),
            'functions': self._extract_functions(script),
            'complexity': self._calculate_complexity(script),
            'best_practices': self._check_best_practices(script),
            'security': self._check_security(script),
            'performance': self._check_performance(script)
        }
        
        return analysis
    
    def _calculate_metrics(self, script: str, lines: List[str]) -> Dict:
        """Calcola metriche base"""
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        comment_lines = [l for l in lines if l.strip().startswith('#')]
        blank_lines = [l for l in lines if not l.strip()]
        
        return {
            'total_lines': len(lines),
            'code_lines': len(code_lines),
            'comment_lines': len(comment_lines),
            'blank_lines': len(blank_lines),
            'comment_ratio': len(comment_lines) / len(lines) if lines else 0
        }
    
    def _extract_cmdlets(self, script: str) -> Dict:
        """Estrae cmdlets utilizzati"""
        cmdlets = self.cmdlet_pattern.findall(script)
        
        cmdlet_counts = defaultdict(int)
        for cmdlet in cmdlets:
            cmdlet_counts[cmdlet] += 1
        
        return {
            'unique': len(cmdlet_counts),
            'total': len(cmdlets),
            'list': dict(cmdlet_counts),
            'top': sorted(cmdlet_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }
    
    def _extract_variables(self, script: str) -> Dict:
        """Estrae variabili"""
        variables = self.variable_pattern.findall(script)
        unique_vars = set(variables)
        
        return {
            'unique': len(unique_vars),
            'total': len(variables),
            'list': list(unique_vars)
        }
    
    def _extract_parameters(self, script: str) -> Dict:
        """Estrae parametri utilizzati"""
        parameters = self.parameter_pattern.findall(script)
        
        param_counts = defaultdict(int)
        for param in parameters:
            param_counts[param] += 1
        
        return {
            'unique': len(param_counts),
            'total': len(parameters),
            'list': dict(param_counts)
        }
    
    def _extract_functions(self, script: str) -> List[Dict]:
        """Estrae definizioni funzioni"""
        function_pattern = re.compile(r'function\s+([A-Za-z0-9_-]+)\s*\{', re.MULTILINE)
        matches = function_pattern.finditer(script)
        
        functions = []
        for match in matches:
            name = match.group(1)
            start_pos = match.start()
            
            functions.append({
                'name': name,
                'line': script[:start_pos].count('\n') + 1,
                'position': start_pos
            })
        
        return functions
    
    def _calculate_complexity(self, script: str) -> Dict:
        """Calcola complessità ciclomatica"""
        # Keywords che aumentano complessità
        complexity_keywords = ['if', 'elseif', 'switch', 'while', 'for', 'foreach', 'catch', '&&', '||']
        
        complexity = 1  # Base complexity
        
        for keyword in complexity_keywords:
            # Case insensitive search
            pattern = re.compile(rf'\b{keyword}\b', re.IGNORECASE)
            matches = pattern.findall(script)
            complexity += len(matches)
        
        # Calcola complessità per funzione
        functions = self._extract_functions(script)
        function_complexity = {}
        
        for func in functions:
            func_name = func['name']
            # Stima complessità funzione (semplificata)
            function_complexity[func_name] = complexity / max(len(functions), 1)
        
        return {
            'total': complexity,
            'rating': self._complexity_rating(complexity),
            'per_function': function_complexity
        }
    
    def _complexity_rating(self, complexity: int) -> str:
        """Valuta complessità"""
        if complexity <= 5:
            return "Simple"
        elif complexity <= 10:
            return "Moderate"
        elif complexity <= 20:
            return "Complex"
        else:
            return "Very Complex"
    
    def _check_best_practices(self, script: str) -> List[str]:
        """Verifica best practices"""
        issues = []
        
        # Check 1: CmdletBinding
        if 'function' in script.lower() and '[CmdletBinding()]' not in script:
            issues.append("Functions should use [CmdletBinding()] for advanced features")
        
        # Check 2: Error handling
        if ('function' in script.lower() or 'cmdlet' in script.lower()) and 'try' not in script.lower():
            issues.append("Consider adding try-catch error handling")
        
        # Check 3: Verbose output
        if 'function' in script.lower() and 'Write-Verbose' not in script:
            issues.append("Add Write-Verbose for better debugging")
        
        # Check 4: Help comments
        if 'function' in script.lower() and '<#' not in script:
            issues.append("Add comment-based help for functions")
        
        # Check 5: Parameter validation
        if 'param(' in script.lower() and '[ValidateNotNull' not in script:
            issues.append("Consider adding parameter validation")
        
        return issues
    
    def _check_security(self, script: str) -> List[str]:
        """Verifica problemi di sicurezza"""
        warnings = []
        
        # Check hardcoded credentials
        if re.search(r'password\s*=\s*["\'][^"\']+["\']', script, re.IGNORECASE):
            warnings.append("Possible hardcoded password detected")
        
        # Check Invoke-Expression
        if 'Invoke-Expression' in script or 'iex' in script:
            warnings.append("Invoke-Expression can be dangerous - validate input carefully")
        
        # Check ExecutionPolicy bypass
        if 'ExecutionPolicy Bypass' in script:
            warnings.append("Bypassing execution policy - ensure this is intended")
        
        # Check remote commands
        if 'Invoke-Command' in script and '-ComputerName' in script:
            warnings.append("Remote command execution detected - ensure proper authentication")
        
        return warnings
    
    def _check_performance(self, script: str) -> List[str]:
        """Suggerimenti performance"""
        suggestions = []
        
        # Check pipeline vs foreach
        if script.count('foreach') > script.count('ForEach-Object'):
            suggestions.append("Consider using ForEach-Object in pipelines for better performance")
        
        # Check Where-Object
        if script.count('Where-Object') > 5:
            suggestions.append("Multiple Where-Object calls can be combined for better performance")
        
        # Check array concatenation in loops
        if '+=' in script and ('for' in script or 'foreach' in script):
            suggestions.append("Avoid += in loops - use ArrayList or collections for better performance")
        
        return suggestions


# Quick utility functions

def quick_cmdlet(verb: str, noun: str, param_name: str = "InputObject",
                param_type: str = "string", logic: str = "Write-Output $InputObject") -> str:
    """Genera rapidamente un cmdlet semplice"""
    gen = PowerShellScriptGenerator()
    return gen.generate_cmdlet(
        verb=verb,
        noun=noun,
        parameters=[{
            'name': param_name,
            'type': param_type,
            'mandatory': True,
            'pipeline': True
        }],
        synopsis=f"{verb} {noun}",
        process_block=logic
    )


def quick_function(name: str, params: List[str], body: str) -> str:
    """Genera rapidamente una funzione"""
    gen = PowerShellScriptGenerator()
    parameters = [{'name': p, 'type': 'object', 'mandatory': False} for p in params]
    return gen.generate_function(name, parameters, f"{name} function", body)


if __name__ == "__main__":
    # Demo
    print("🤖 PowerShell Advanced Generator Demo\n")
    print("=" * 80)
    
    gen = PowerShellScriptGenerator()
    
    # Genera cmdlet
    print("\n1. CMDLET GENERATION")
    print("-" * 80)
    cmdlet = gen.generate_cmdlet(
        verb="Get",
        noun="UserData",
        parameters=[
            {'name': 'UserName', 'type': 'string', 'mandatory': True, 'pipeline': True},
            {'name': 'Detailed', 'type': 'switch', 'mandatory': False}
        ],
        synopsis="Retrieves user data from system",
        process_block='''$user = Get-ADUser -Identity $UserName
if ($Detailed) {
    Get-ADUser -Identity $UserName -Properties *
} else {
    $user
}'''
    )
    print(cmdlet[:500] + "...")
    
    # Analizza script
    print("\n\n2. SCRIPT ANALYSIS")
    print("-" * 80)
    analyzer = PowerShellAnalyzer()
    analysis = analyzer.analyze_script(cmdlet)
    print(f"Cmdlets found: {analysis['cmdlets']['unique']}")
    print(f"Variables: {analysis['variables']['unique']}")
    print(f"Complexity: {analysis['complexity']['total']} ({analysis['complexity']['rating']})")
    print(f"Best practices issues: {len(analysis['best_practices'])}")
    
    print("\n" + "=" * 80)
    print("✅ Demo completed!")
