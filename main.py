import os
import json
import sys
from pathlib import Path
import re

stem_regex = r'.*\(\d+\)\..*'


def get_alike_regex(filename):
    tokens = filename.split(".")
    name = re.escape(".".join(tokens[0:len(tokens) - 1]))
    ext = re.escape(tokens[len(tokens) - 1])
    return fr".*{name}( (\d{{1,2}}\.){{2}}\d{{1,2}} PM)+\.{ext}\..*"


def get_alike_regex_with_duplication(filename):
    return fr".*{re.escape(filename)}( (\d{{1,2}}\.){{2}}\d{{1,2}} PM)+\..*"


def move_duplication_string(path):
    pattern = r"(.*)\((.*?)\)(\..*)"
    match = re.search(pattern, path)
    if match:
        new_path = match.group(1) + match.group(3) + "(" + match.group(2) + ")"
        return new_path
    else:
        return path


def get_alike_json(path):
    dir_path = os.path.dirname(path)
    file_name = os.path.basename(path)
    jsons = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.json')]
    regex = get_alike_regex(file_name)
    for json in jsons:
        if re.match(regex, json):
            return json

    # Try with duplication

    file_name = os.path.basename(move_duplication_string(path))
    regex = get_alike_regex_with_duplication(file_name)
    for json in jsons:
        if re.match(regex, json):
            return json


def update_image_creation_time(image_path):
    # Get the timestamp from the JSON file
    json_path = Path(move_duplication_string(image_path) + ".json")
    json_data = None
    try:
        with open(json_path, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        try:
            with open(Path(image_path + ".json"), 'r') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            try:
                # Remove the "-edited" from the file name
                no_edited = image_path.replace("-edited", "")
                with open(Path(no_edited + ".json"), 'r') as f:
                    json_data = json.load(f)
            except FileNotFoundError:
                try:
                    with open(Path(get_alike_json(image_path)), 'r') as f:
                        json_data = json.load(f)
                except FileNotFoundError:
                    print(f"Could not find JSON file for {image_path}")
                    return
                # os.remove(image_path)

    timestamp = json_data['photoTakenTime']['timestamp']
    # Convert the timestamp from string to float
    timestamp = float(timestamp)
    # Convert the timestamp to a datetime object
    # dt = datetime.fromtimestamp(timestamp)
    # Update the image's creation time
    os.utime(image_path, (timestamp, timestamp))


path = sys.argv[1]

for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if not filename.endswith('.json') and filename != '.DS_Store':
            file_path = os.path.join(dirpath, filename)
            try:
                update_image_creation_time(file_path)
            except:
                print("Could not update image creation time for " + file_path)