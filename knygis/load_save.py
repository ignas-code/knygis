import os
import pickle
from library import Library

pickle_file_path = 'knygis/lib.pickle'

def save(lib):
    with open(pickle_file_path, 'wb') as file:
        pickle.dump(lib, file)

def load():
    with open(pickle_file_path, 'rb') as file:
        lib = pickle.load(file)
    return lib

def initial_load():
    if os.path.exists(pickle_file_path):
        lib = load()
        return lib
    else:
        lib = Library()
        save(lib)
        return lib