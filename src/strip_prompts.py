import ast

# Strip function bodies (comments and docstrings) from Python functions, leaving only imports and function prototypes
def strip_code(source: str, solution: str) -> str:
    # Parse prompt string into abstract syntax tree of different code components
    module = ast.parse(source)
    new_body = []

    # Iterate through each node in the module body, keeping what is important
    for node in module.body:
        # Keep import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            new_body.append(node)
        # Keep function definitions
        elif isinstance(node, ast.FunctionDef):
            new_body.append(ast.FunctionDef(
                name=node.name,
                args=node.args,
                # Have to set the body manually
                body=None,
                decorator_list=node.decorator_list,
                returns=node.returns,
            ))
        elif isinstance(node, ast.AsyncFunctionDef):
            new_body.append(ast.AsyncFunctionDef(
                name=node.name,
                args=node.args,
                # Have to set the body manually
                body=None,
                decorator_list=node.decorator_list,
                returns=node.returns,
            ))

    new_module = ast.Module(body=new_body, type_ignores=[])
    ast.fix_missing_locations(new_module)
    
    out_lines = []
    # Manually reconstruct the code from the new AST. ast.unparse was unable to support partial ASTs
    for n in new_body:
        # Build import statements
        if isinstance(n, ast.Import):
            for a in n.names:
                out_lines.append(f"import {a.name}" + (f" as {a.asname}" if a.asname else ""))
        # Build from ... import ... statements
        elif isinstance(n, ast.ImportFrom):
            module_name = n.module or ''
            level = '.' * n.level
            names = ', '.join((f"{a.name} as {a.asname}" if a.asname else a.name) for a in n.names)
            out_lines.append(f"from {level}{module_name} import {names}")
        # Build function definitions
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            prefix = 'async ' if isinstance(n, ast.AsyncFunctionDef) else ''
            arg_names = [a.arg for a in n.args.args]
            ret = ''
            if getattr(n, 'returns', None) is not None:
                try:
                    ret = ' -> ' + ast.unparse(n.returns)
                except Exception:
                    ret = ''
            out_lines.append(f"{prefix}def {n.name}({', '.join(arg_names)}){ret}:")
            # Insert the provided solution from the dataset as the function body
            sol_lines = solution.splitlines()
            if sol_lines:
                for s in sol_lines:
                    out_lines.append(s)
    return '\n'.join(out_lines)

