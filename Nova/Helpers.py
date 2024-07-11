from contextlib import redirect_stdout, redirect_stderr, contextmanager
from io import StringIO
import sys

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