def read_file(file_location):
    # Read text file, concatenate all lines into 1
    with open(file_location, 'rb') as f:
        data = f.read().replace('\n', " ")
    return data
