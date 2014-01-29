from collections import deque
import json
import os
import sys
import unicode_csv

from fetch_metadata import DATA_PATH, JSON_DATA_PATH

CSV_DATA_PATH = os.path.join(DATA_PATH, 'csv')
MASTER_CSV_FILE_NAME = 'playviz.csv'

def get_json_file_names(path=JSON_DATA_PATH):
    try:
        result = os.listdir(path)
    except OSError:
        sys.stderr.write("json data directory does not exist")
        sys.exit()
    if not result:
        sys.stderr.write("json data directory is empty")
        sys.exit()
    sys.stdout.write("json dir contains {count} files:\n    {files}\n".format(
        count=len(result),
        files=", ".join(result)
    ))
    return result

def get_csv_file_names(path=CSV_DATA_PATH):
    try:
        result = os.listdir(path)
    except OSError:
        os.mkdir(path)
        sys.stdout.write("csv dir created\n")
        result = []
    sys.stdout.write("csv dir contains {count} files:\n    {files}\n".format(
        count=len(result),
        files=", ".join(result)
    ))
    return result

def make_csv_file(file_name, write_master_headers):
    f = open(os.path.join(JSON_DATA_PATH, file_name), 'r')
    json_body = json.loads(f.read())

    f = open(os.path.join(CSV_DATA_PATH, file_name), 'w')
    csv_writer = unicode_csv.UnicodeWriter(f)
    master_f = open(os.path.join(CSV_DATA_PATH, MASTER_CSV_FILE_NAME), 'a')
    master_csv_writer = unicode_csv.UnicodeWriter(master_f)

    sys.stdout.write("Writing csv output for {file_name}\n".format(file_name=file_name))

    headers = deque(('Name', 'Artist', 'Length', \
               'Popularity', 'Album name', 'Album year'))

    csv_writer.writerow(headers)
    if write_master_headers:
        headers.appendleft('User')
        master_csv_writer.writerow(headers)

    for item in json_body:
        track = item['track']
        row = deque([
            track['name'],
            track['artists'][0]['name'],
            str(track['length']),
            track['popularity'],
            track['album']['name'],
            track['album']['released'],
        ])
        csv_writer.writerow(row)
        row.appendleft(file_name)
        master_csv_writer.writerow(row)
    f.close()
    master_f.close()
    sys.stdout.write("{master_file_name} updated\n".format(master_file_name=MASTER_CSV_FILE_NAME))
    return file_name

def make_csv_files(file_names, write_master_headers):
    created = []
    for file_name in file_names:
        created.append(make_csv_file(file_name, write_master_headers))
        write_master_headers = False
    return created

def main():
    json_file_names = get_json_file_names()
    csv_file_names = get_csv_file_names()
    file_names = set(json_file_names) - set(csv_file_names)
    if not file_names:
        sys.stdout.write("All csv files already exist\n")
        sys.exit()
    sys.stdout.write("{count} csv files need creating\n".format(count=len(file_names)))
    created = make_csv_files(
        file_names,
        write_master_headers=not bool(csv_file_names)
    )
    sys.stdout.write("{count} csv files created:\n    {files}\n".format(
        count=len(created),
        files=", ".join(created)
    ))


if __name__ == "__main__":
    main()
