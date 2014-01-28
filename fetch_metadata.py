import os
import sys

DATA_PATH = 'data'
URI_DATA_PATH = os.path.join(DATA_PATH, 'uris')
JSON_DATA_PATH = os.path.join(DATA_PATH, 'json')

def get_uri_file_names(path=URI_DATA_PATH):
    try:
        result = os.listdir(path)
    except OSError:
        sys.stderror.write("uri data directory does not exist")
        sys.exit()
    if not result:
        sys.stderror.write("uri data directory is empty")
        sys.exit()
    return result

def main():
    uri_file_names = get_uri_file_names()
    sys.stdout.write(", ".join(uri_file_names))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
