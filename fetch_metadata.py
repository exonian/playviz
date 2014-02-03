import json
import os
import requests
import sys

DATA_PATH = 'data'
URI_DATA_PATH = os.path.join(DATA_PATH, 'uris')
JSON_DATA_PATH = os.path.join(DATA_PATH, 'json')

LOOKUP_URL = "http://ws.spotify.com/lookup/1/.json?uri={uri}"
SEARCH_URL = "http://ws.spotify.com/search/1/track.json"

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

def get_json_file_names(path=JSON_DATA_PATH):
    try:
        result = os.listdir(path)
    except OSError:
        os.mkdir(path)
        sys.stdout.write("json dir created\n")
        result = []
    sys.stdout.write("json dir contains {count} files:\n    {files}\n".format(
        count=len(result),
        files=", ".join(result)
    ))
    return result

def get_uris_from_file(file_name):
    f = open(os.path.join(URI_DATA_PATH, file_name), 'r')
    return f.read().split()

def get_track_name(track_name):
    return track_name.replace(' - Remastered', '')

def improve_year(response_json):
    payload = {
        'q': u'artist:"{a}" track:"{t}"'.format(
            a = response_json['track']['artists'][0]['name'],
            t = get_track_name(response_json['track']['name']),
        )
    }
    search_response = requests.get(SEARCH_URL, params=payload)
    years = [track['album']['released'] for track in search_response.json()['tracks']]
    years.sort()
    response_json.update(year_from_search=years[0])
    return response_json

def make_json_file(file_name):
    uris = get_uris_from_file(file_name)
    json_responses = []
    for uri in uris:
        sys.stdout.write("Fetching metadata for {file_name}, {uri}\n".format(
            file_name=file_name,
            uri=uri,
        ))
        response = requests.get(LOOKUP_URL.format(uri=uri))
        json_response = improve_year(response.json())
        json_responses.append(json_response)
    sys.stdout.write("Creating json output for {file_name}\n".format(file_name=file_name))
    full_json = json.dumps(json_responses)
    sys.stdout.write("Writing json output for {file_name}\n".format(file_name=file_name))
    f = open(os.path.join(JSON_DATA_PATH, file_name), 'w')
    f.write(full_json)
    f.close()
    return file_name

def make_json_files(file_names):
    created = []
    for file_name in file_names:
        created.append(make_json_file(file_name))
    return created

def main():
    uri_file_names = get_uri_file_names()
    json_file_names = get_json_file_names()
    file_names = set(uri_file_names) - set(json_file_names)
    if not file_names:
        sys.stdout.write("All json files already exist\n")
        sys.exit()
    sys.stdout.write("{count} json files need creating\n".format(count=len(file_names)))
    created = make_json_files(file_names)
    sys.stdout.write("{count} json files created:\n    {files}\n".format(
        count=len(created),
        files=", ".join(created)
    ))


if __name__ == "__main__":
    main()
