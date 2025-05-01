import os

def get_absolute_path(path):
    return os.path.abspath(path)

def exists(path):
    return os.path.exists(path)
