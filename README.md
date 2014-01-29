playviz
=======

Getting some Spotify playlist data ready for use in Tableau


Installation
------------

Install required python packages using pip, preferably within a virtualenv (for your own sanity):

  `pip install -r requirements.txt`


Usage
-----

Creating the uri file
  - Open a playlist in the Spotify desktop client (the web client doesn't seem to allow selecting of multiple tracks simultaneously)
  - Select all tracks (Click on the first track, then shift-click the last track or press ctrl-a)
  - Right click and select "Copy Spotify URI"
  - Paste the result into a text file and save it in `/data/uris/` with the name you want used for the user (don't bother with an extension)

Fetching the track metadata from Spotify
  - Run `python fetch_metadata.py` to create json files (albeit ones without any sort of file extension) in `/data/json/` for each uri file that doesn't already have one

Exporting to csv
  - Run `python export_csv_files.py` to create csv files (again without a file extension) in `/data/csv/` for each json file that doesn't already have one, and to mirror the data to `/data/csv/playviz.csv`


Care instructions
-----------------

Only data written to a new playlist csv file is mirrored to `/data/csv/playviz.csv`, so if you delete playviz.csv but not the individual csv files you will end up with an incomplete playviz.csv next time you run export_csv_files; if you have to delete playviz.csv, delete all csv files with it.
