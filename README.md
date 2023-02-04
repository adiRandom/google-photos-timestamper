# google-photos-timestamper

Usign [Google Takeout](https://takeout.google.com/settings/takeout) you can export your photos saved in Google Photos to migrate wherever else you want
However, the while on google servers, the metadata from the files gets stripped from the images and put in separate JSONs. 

This script is meant to add back the creation time of the images from their associated JSON files.
The script can be easily modified to extract any piece of metadata from the image json.

## Before running
Before running the script I suggest downloading all the images you want to pull of Google Photos and running the script once for all of them. 
I noticed that Google Takeout doesn't make sure thatboth the image and it's json file are in the same archive from the split download. 

If you run the script on each archive at a time you might end up with photos that weren't fixed.


## Usage

Just call the script with the path to the folder holding images. The script will recursively look for images and associated json files in the provided path.

`main.py path/to.images`


**Note**

The script expects that the folders searched only contain image files and their associated jsons. 
There is no filtering in place to only look for image file extensions


## JSON naming

At first, it lookes like for each `Image.ext` there is an associated `Image.ext.json` file. 
However, while working on this I encoutered differet namings and included rules for them.

1. Duplicate files

If you have 2 images with the same name `Image.jpeg`, on your disk you'll have `Image.jpeg` and `Image(1).jpeg`. 
However, the JSON files will be names `Image.jpeg.json` and `Image.jpeg(1).json`

2. Edited images

Edited images from Google Photos get the `-Edited` suffix. But they don't also get an associated JSON. Instead they have the JSON of the original photo.
So `Image-Editate.jpeg` will have its metadata in `Image.jpeg.json`

3. JSON Names that don't perfectly match the name of the image

This rule might not apply to you. I think due to some wierd Mac OS bug I ended up with some JSON files that also contained some timestamps in their names.
So I included a rule that given an image that has no perfect match for its json after checking the above 2 rules, 
it looks for the first JSON file that contains the name of the image file
