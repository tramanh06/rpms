import os
import io
import glob
import json

def read_file(file_location, sep=" "):
    ' Read text file, concatenate all lines into 1 '
    with io.open(file_location, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read().replace('\n', sep)
    return data


def read_json_file(file_location):
    with open(file_location) as f:
        data = json.load(f)
    return data


def write_to_file(file_location, data):
    with open(file_location, 'w') as f:
        f.write(data)


def write_to_json_file(file_location, data):
    with open(file_location, 'wb') as f:
        json.dump(data, f)

def is_folder_exists_create_otherwise(outDIR):
    # Check if output folder has been created. Create otherwise
    try:
        os.makedirs(outDIR)
    except OSError:
        if not os.path.isdir(outDIR):
            raise


def extract_all_files_with_pattern(directory, pattern):
    all_txt = [read_file(filename) for filename in glob.glob(directory + pattern)]
    return all_txt


def flatten(l):
    return [item for sublist in l for item in sublist]
