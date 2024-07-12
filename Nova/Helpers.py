from contextlib import redirect_stdout, redirect_stderr, contextmanager
from io import StringIO
import sys
import builtins
from types import ModuleType

def suppress_output_decorator(func):
    def wrapper(*args, **kwargs):
        # Redirect stdout and stderr to a string buffer
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            result = func(*args, **kwargs)
        return result
    return wrapper

@contextmanager
def suppress_output():
    # Save the original stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    # Redirect stdout and stderr to a string buffer
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    
    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer
    
    try:
        yield
    finally:
        # Restore the original stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr

#Used to limit which libaries a Module can access
class RestrictedImporter:
    def __init__(self, disallowed_modules):
        self.disallowed_modules = set(disallowed_modules)
        self.original_import = builtins.__import__

    def custom_import(self, name, *args, **kwargs):
        if name in self.disallowed_modules:
            raise ImportError(f"Import of '{name}' is not allowed")
        return self.original_import(name, *args, **kwargs)

    def apply(self):
        builtins.__import__ = self.custom_import

    def restore(self):
        builtins.__import__ = self.original_import

def run_file_with_restricted_imports(file_path, disallowed_modules):
    importer = RestrictedImporter(disallowed_modules)
    importer.apply()
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            exec(code, {'__name__': '__main__'})
    finally:
        importer.restore()