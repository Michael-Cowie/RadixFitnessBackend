import sys
from os.path import abspath, dirname, join


def setup_python_path():
    sys.path.append(abspath(join(dirname(__file__), "..")))  # backend directory
    sys.path.append(abspath(join(dirname(__file__), "..", "..", "..")))  # root directory
