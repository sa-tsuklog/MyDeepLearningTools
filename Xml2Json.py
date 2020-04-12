import os
import glob
import xml.etree.ElementTree as ET
import xmltodict
import json
import re
from xml.dom import minidom
from collections import OrderedDict

def XML2JSON(xmlFiles):
    attrDict = dict()

#    attrDict["categories"]=[{"supercategory":"none","id":1,"name":"aeroplane"},
#                    {"supercategory":"none","id":2,"name":"bicycle"},
#                    {"supercategory":"none","id":3,"name":"bird"},
#                    {"supercategory":"none","id":4,"name":"boat"},
#                {"supercategory":"none","id":5,"name":"bottle"},
#                {"supercategory":"none","id":6,"name":"bus"},
#                {"supercategory":"none","id":7,"name":"car"},
#                {"supercategory":"none","id":8,"name":"cat"},
#                {"supercategory":"none","id":9,"name":"chair"},
#                {"supercategory":"none","id":10,"name":"cow"},
#                {"supercategory":"none","id":11,"name":"diningtable"},
#                {"supercategory":"none","id":12,"name":"dog"},
#                {"supercategory":"none","id":13,"name":"horse"},
#                {"supercategory":"none","id":14,"name":"motorbike"},
#                {"supercategory":"none","id":15,"name":"person"},
#                {"supercategory":"none","id":16,"name":"pottedplant"},
#                {"supercategory":"none","id":17,"name":"sheep"},
#                {"supercategory":"none","id":18,"name":"sofa"},
#                {"supercategory":"none","id":19,"name":"train"},
#                {"supercategory":"none","id":20,"name":"tvmonitor"}]

#    attrDict["categories"]=[{"supercategory":"none","id":1,"name":"aircraft"}]

    attrDict["categories"]=[{"supercategory":"none","id":1,"name":"A-10"},
                            {"supercategory":"none","id":2,"name":"F-14"},
                            {"supercategory":"none","id":3,"name":"F-15"},
                            {"supercategory":"none","id":4,"name":"F-16"},
                            {"supercategory":"none","id":5,"name":"FA-18"},
                            {"supercategory":"none","id":6,"name":"M-2000"},
                            {"supercategory":"none","id":7,"name":"Su-27"}]


    images = list()
    annotations = list()
    image_id = 0
    id1 = 1
    for file in xmlFiles:    
        #image_id = image_id + 1      
        image_id = re.sub("\\D","",file)
        print("Debug:",image_id,",",file)
        annotation_path=file
        image = dict()
        doc = xmltodict.parse(open(annotation_path).read(), force_list=('object'))
        image['file_name'] = str(doc['annotation']['filename'])
        image['height'] = int(doc['annotation']['size']['height'])
        image['width'] = int(doc['annotation']['size']['width'])
        image['id'] = image_id
        print ("File Name: {} and image_id {}".format(file, image_id))
        images.append(image)

        if 'object' in doc['annotation']:
            for obj in doc['annotation']['object']:
                for value in attrDict["categories"]:
                    annotation = dict()          
                    if str(obj['name']) == value["name"]:
                        annotation["iscrowd"] = 0
                        annotation["image_id"] = image_id
                        x1 = int(float(obj["bndbox"]["xmin"]))  - 1
                        y1 = int(float(obj["bndbox"]["ymin"])) - 1
                        x2 = int(float(obj["bndbox"]["xmax"])) - x1
                        y2 = int(float(obj["bndbox"]["ymax"])) - y1                         
                        annotation["bbox"] = [x1, y1, x2, y2]
                        annotation["area"] = float(x2 * y2)
                        annotation["category_id"] = value["id"]
                        annotation["ignore"] = 0
                        annotation["id"] = id1
                        annotation["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
                        id1 +=1
                        annotations.append(annotation)

            else:
                print("File: {} doesn't have any object".format(file))

        else:
            print("File: {} not found".format(file))


    attrDict["images"] = images    
    attrDict["annotations"] = annotations
    attrDict["type"] = "instances"
    jsonString = json.dumps(attrDict,indent=4,sort_keys=True,separators=(",",":"))
    with open("train.json", "w") as f:
        f.write(jsonString)


path="./annotations/"
trainXMLFiles=glob.glob(os.path.join(path, '*.xml'))
XML2JSON(trainXMLFiles)

