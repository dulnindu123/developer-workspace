import ast
import re

class PythonVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = []
        self.functions = []
        self.dependencies = []

    def visit_ClassDef(self, node):
        self.classes.append({
            "name": node.name,
            "start_line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno)
        })
        # Check inheritance
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.dependencies.append({
                    "source": node.name,
                    "target": base.id,
                    "type": "inheritance"
                })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append({
            "name": node.name,
            "start_line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno)
        })
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.dependencies.append({
                "source": "unknown_context", # Simplified for MVP
                "target": node.func.id,
                "type": "call"
            })
        elif isinstance(node.func, ast.Attribute):
            self.dependencies.append({
                "source": "unknown_context",
                "target": node.func.attr,
                "type": "method_call"
            })
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.dependencies.append({
                "source": "module_scope",
                "target": alias.name,
                "type": "import"
            })
        self.generic_visit(node)

def parse_python(code: str):
    visitor = PythonVisitor()
    try:
        tree = ast.parse(code)
        visitor.visit(tree)
    except SyntaxError:
        pass # Handle invalid code gracefully
    return visitor.classes, visitor.functions, visitor.dependencies

def parse_regex_fallback(code: str, language: str):
    """Fallback Regex Parsers for Java, JS, HTML, CSS as requested for MVP"""
    classes = []
    functions = []
    dependencies = []
    
    # Very rudimentary regex for MVP demonstration
    if language.lower() in ["java", "javascript", "js"]:
        # Match class declarations
        for match in re.finditer(r'class\s+([A-Za-z0-9_]+)', code):
            classes.append({"name": match.group(1), "start_line": code[:match.start()].count('\n') + 1, "end_line": 0})
        # Match function declarations
        for match in re.finditer(r'(?:function\s+|public\s+[a-z<>\[\]]+\s+)([A-Za-z0-9_]+)\s*\(', code):
            functions.append({"name": match.group(1), "start_line": code[:match.start()].count('\n') + 1, "end_line": 0})
            
    elif language.lower() in ["html", "css"]:
        # HTML/CSS don't have traditional classes/functions in the AST sense,
        # but we can extract IDs and Classes as nodes for visualization.
        for match in re.finditer(r'(id|class)="([^"]+)"', code):
            classes.append({"name": match.group(2), "start_line": code[:match.start()].count('\n') + 1, "end_line": 0})

    return classes, functions, dependencies

def analyze_code(code: str, language: str):
    if language.lower() == "python":
        return parse_python(code)
    else:
        return parse_regex_fallback(code, language)
