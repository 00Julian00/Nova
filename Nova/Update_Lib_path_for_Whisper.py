import pkgutil
import re
from pathlib import Path

# patch whisper on file not find error
# https://github.com/carloscdias/whisper-cpp-python/pull/12
try:
    import whisper_cpp_python
except FileNotFoundError:
    regex = r"(\"darwin\":\n\s*lib_ext = \")\.so(\")"
    subst = "\\1.dylib\\2"

    print("fixing and re-importing whisper_cpp_python...")
    # load whisper_cpp_python and substitute .so with .dylib for darwin
    package = pkgutil.get_loader("whisper_cpp_python")
    whisper_path = Path(package.path)
    whisper_cpp_py = whisper_path.parent.joinpath("whisper_cpp.py")
    content = whisper_cpp_py.read_text()
    result = re.sub(regex, subst, content, 0, re.MULTILINE)
    whisper_cpp_py.write_text(result)

    import whisper_cpp_python