import os


def read_file(file_location):
    ' Read text file, concatenate all lines into 1 '
    with open(file_location, 'rb') as f:
        data = f.read().replace('\n', " ")
    return data


def write_to_file(file_location, data):
    with open(file_location, 'w') as f:
        f.write(data)


def is_folder_exists_create_otherwise(outDIR):
    # Check if output folder has been created. Create otherwise
    try:
        os.makedirs(outDIR)
    except OSError:
        if not os.path.isdir(outDIR):
            raise
