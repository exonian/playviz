import os
import sys

DATA_PATH = 'data'
URI_DATA_PATH = os.path.join(DATA_PATH, 'uris')
JSON_DATA_PATH = os.path.join(DATA_PATH, 'json')

def get_uri_file_names(path=URI_DATA_PATH):
    try:
        result = os.listdir(path)
    except OSError:
        sys.stderr.write("uri data directory does not exist")
        sys.exit()
    if not result:
        sys.stderr.write("uri data directory is empty")
        sys.exit()
    sys.stdout.write("uri dir contains {count} files:\n    {files}\n".format(
        count=len(result),
        files=", ".join(result)
    ))
    return result

def main():
    uri_file_names = get_uri_file_names()


if __name__ == "__main__":
    main()
