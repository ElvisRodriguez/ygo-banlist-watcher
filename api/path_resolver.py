import os
from pathlib import Path

def get_full_path(script, filename):
    """Get the absolute path of a file in a script's directory.
    Args:
        script (str): __file__ attribute of a python script.
        filename (str): Filename of a file in script's directory.
    Returns:
        full_path (os.path): Absolute path to filename.
    """
    real_path = os.path.realpath(script)
    parent_directory = Path(real_path).parent.absolute()
    full_path = os.path.join(parent_directory, filename)
    return full_path