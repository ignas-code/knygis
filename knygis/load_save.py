import os
import pickle
from library import Library

pickle_file_path = 'knygis/lib.pickle'

def save(lib):
    with open(pickle_file_path, 'wb') as file:
        pickle.dump(lib, file)
    # print(f"Library object saved to {file_path}")

def load():
    with open(pickle_file_path, 'rb') as file:
        lib = pickle.load(file)
    # print(f"Library object loaded from {file_path}")
    return lib

def initial_load():
    if os.path.exists(pickle_file_path):
        lib = load()
        return lib
    else:
        lib = Library()
        save(lib)
        return lib