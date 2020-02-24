#!/usr/bin/env python
# coding: utf-8
#this file smashes all lbbx images into a coco formated json

import json
from PIL import Image
import os
import re
from olatools import intify_filename

with open('03_config/coco_template.json', 'r') as f:
    coco_schema = json.load(f)

img_dir = "/Users/ola/code/grisehale_nmbu/media/coco_test/batch1"

for filename in os.listdir(img_dir):
    im = Image.open(os.path.join(img_dir,filename))
    width, height = im.size
    id = int(intify_filename(filename))

    appendant_img =     {
      "id" : id,
      "width" : width,
      "height" : height,
      "file_name" : filename,
      "license" : 1,
      "flickr_url" : "not available",
      "coco_url" : "not available",
      "date_captured" : "2019-08-15T00:00:00.000Z"
    }
    coco_schema["images"].append(appendant_img)


with open("02_output/batch1_coco_images_no_annotations.json", 'w') as wf:
    json.dump(coco_schema, wf)




#this file smashes all lbbx annotations into a coco formatted file


import json
import os
from olatools import create_BB_from_polygon, create_polygon_from_point, intify_filename, ret_area_of_bb

import pprint
pp = pprint.PrettyPrinter(indent=4)

#batch1folder = "/Users/ola/code/grisehale_nmbu/media/coco_test/batch1"
#annotationsFolder = "/Users/ola/code/grisehale_nmbu/sandbox/annotations"
annotationsFolder = "./01_lbbx_annotations"
lbbxAnnFile = "export-2019-08-19T10_26_58.766Z.json"
cocoDestFile = "02_output/batch1_coco_images_no_annotations.json"    #   "coco_template.json"

with open(cocoDestFile, 'r') as rf:
        coco_json = json.load(rf)

with open(os.path.join(annotationsFolder,lbbxAnnFile), 'r') as wf:
    annotated_images = json.load(wf)           #, strict=False)

#change this to include/exclude quality segments
category_id_enum = {
    "pig-lying-bad-visibility":1,
    "pig-lying-good-visibility":1,
    "pig-standing-bad-visibility":1,
    "pig-standing-good-visibility":1,
    "face-good-visibility":2,
    "face-bad-visibility":2,
    "tail-curl-standing":3,
    "tail-straight-standing":3,
    "tail-uncertain-or-lying":3,
}

#remove unncomplete elements (often "skipped" in annotaition)
for element in reversed(annotated_images):
    if len(element)<18:
        annotated_images.remove(element)

annotation_id_counter = 0

for element in annotated_images:
    img_file_name = element["External ID"]
    image_id = intify_filename(img_file_name)

    for present_label in element["Label"]: #"Label" is a list of present label classes per image
        category_id = category_id_enum[present_label]
        if "tail" in present_label: # this means that the lable is a point, we need to convert to polygon/bb
            for label_instance in element["Label"][present_label]: #
                segmentation = [[]]

                segmentation[0].append(int(label_instance["geometry"]["x"]))
                segmentation[0].append(int(label_instance["geometry"]["y"]))

                polygon = create_polygon_from_point(segmentation[0])
                bbox = create_BB_from_polygon(polygon[0])
                area = ret_area_of_bb(bbox)

                appendant = {
                  "id" : annotation_id_counter,
                  "image_id" : image_id,
                  "category_id" : category_id,
                  "segmentation" : polygon,
                  "area" : area,
                  "bbox" : bbox,
                  "iscrowd" : 0
                }
                coco_json["annotations"].append(appendant)
                annotation_id_counter = annotation_id_counter + 1

        else:
            labinstcount = 0
            for label_instance in element["Label"][present_label]: #"Label" is actually a list of the different label classes present in the image
                labinstcount = labinstcount + 1
                for geometry in range(len(label_instance)): #geometry counts the numer of polygon per lable (usually just 1 in our case)
                    segmentation = [[]]
                    for XY_coordinate in label_instance["geometry"]:
                        #print("XY: ", XY_coordinate)
                        segmentation[0].append(XY_coordinate["x"])
                        segmentation[0].append(XY_coordinate["y"])

                bbox = create_BB_from_polygon(segmentation[0])
                area = ret_area_of_bb(bbox)

                appendant = {
                  "id" : annotation_id_counter,
                  "image_id" : image_id,
                  "category_id" : category_id,
                  "segmentation" : segmentation,
                  "area" : area,
                  "bbox" : bbox,
                  "iscrowd" : 0
                }
                coco_json["annotations"].append(appendant)
                annotation_id_counter = annotation_id_counter + 1

with open("02_output/cocoifyed_export_images+annotations.json", 'w') as wf:
    json.dump(coco_json, wf)
