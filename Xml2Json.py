import os
import glob
import xml.etree.ElementTree as ET
import xmltodict
import json
import re
from xml.dom import minidom
from collections import OrderedDict

KEYPOINT_LENGTH = 3

def getEmptyAnnotation():
    annotation = dict()
    
    annotation["iscrowd"] = 0
    annotation["image_id"] = 0
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0                         
    annotation["bbox"] = [x1, y1, x2, y2]
    annotation["area"] = float(x2 * y2)
    annotation["category_id"] = 0
    annotation["ignore"] = 0
    annotation["id"] = 0
    annotation["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
    annotation["keypoints"] = [0,0,0]*KEYPOINT_LENGTH
    annotation["num_keypoints"] = 0
    
    return annotation

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

#     attrDict["categories"]=[{"supercategory":"none","id":1,"name":"A-10"},
#                             {"supercategory":"none","id":2,"name":"F-14"},
#                             {"supercategory":"none","id":3,"name":"F-15"},
#                             {"supercategory":"none","id":4,"name":"F-16"},
#                             {"supercategory":"none","id":5,"name":"FA-18"},
#                             {"supercategory":"none","id":6,"name":"M-2000"},
#                             {"supercategory":"none","id":7,"name":"Su-27"}]

    attrDict["categories"]=[{"supercategory":"none","id":1,"name":"A-10","keypoints":["A-10_nose","A-10_rightWingtip","A-10_leftWingtip"],"skelton":[[1,2],[1,3],[2,3]]}]
    invisibleKeypoints = [{"name":"A-10","keypoints":["A-10_nose_invisible","A-10_rightWingtip_invisible","A-10_leftWingtip_invisible"]}]

    images = list()
    annotations = list()
    image_id = 0
    id1 = 1
    for file in xmlFiles:    
        #image_id = image_id + 1      
        image_id = re.sub("\\D","",file)
        
        annotation_path=file
        image = dict()
        doc = xmltodict.parse(open(annotation_path).read(), force_list=('object'))
        image['file_name'] = str(doc['annotation']['filename'])
        image['height'] = int(doc['annotation']['size']['height'])
        image['width'] = int(doc['annotation']['size']['width'])
        image['id'] = image_id
        print ("File Name: {} and image_id {}".format(file, image_id))
        images.append(image)
        
        annotationsInXml = dict()
        
        if 'object' in doc['annotation']:
            for obj in doc['annotation']['object']:
                for idx,value in enumerate(attrDict["categories"]):
                    name = value["name"]
                    if name == str(obj['name']):
                        if(annotationsInXml.get(name) == None):
                            annotationsInXml[name] = getEmptyAnnotation()
                        
                        
                        annotationsInXml[name]["iscrowd"] = 0
                        annotationsInXml[name]["image_id"] = image_id
                        x1 = int(float(obj["bndbox"]["xmin"]))  - 1
                        y1 = int(float(obj["bndbox"]["ymin"])) - 1
                        x2 = int(float(obj["bndbox"]["xmax"])) - x1
                        y2 = int(float(obj["bndbox"]["ymax"])) - y1                         
                        annotationsInXml[name]["bbox"] = [x1, y1, x2, y2]
                        annotationsInXml[name]["area"] = float(x2 * y2)
                        annotationsInXml[name]["category_id"] = value["id"]
                        annotationsInXml[name]["ignore"] = 0
                        annotationsInXml[name]["id"] = id1
                        annotationsInXml[name]["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
                        id1 +=1
                        
                    for i,kpName in enumerate(attrDict["categories"][idx]["keypoints"]):
                        if(kpName == str(obj["name"])):
                            if(annotationsInXml.get(name) == None):
                                annotationsInXml[name] = getEmptyAnnotation()
                            
                            x = int((float(obj["bndbox"]["xmin"]) + float(obj["bndbox"]["xmax"]))/2)
                            y = int((float(obj["bndbox"]["ymin"]) + float(obj["bndbox"]["ymax"]))/2)
                            
                            annotationsInXml[name]["keypoints"][i*3 + 0] = x
                            annotationsInXml[name]["keypoints"][i*3 + 1] = y
                            annotationsInXml[name]["keypoints"][i*3 + 2] = 2
                            annotationsInXml[name]["num_keypoints"] += 1
                
                for value in invisibleKeypoints:
                    name == value["name"]
                    
                    
                    
                    for i,kpName in enumerate(value["keypoints"]):
                        
                        print("kpName:",kpName,", obj-name",str(obj["name"]))
                        
                        if(kpName == str(obj["name"])):
                            print("--------------------")
                            print("kpName:",kpName)
                            print("objName:",str(obj["name"]))
                            
                            if(annotationsInXml.get(name) == None):
                                annotationsInXml[name] = getEmptyAnnotation()
                            
                            x = int((float(obj["bndbox"]["xmin"]) + float(obj["bndbox"]["xmax"]))/2)
                            y = int((float(obj["bndbox"]["ymin"]) + float(obj["bndbox"]["ymax"]))/2)
                            
                            annotationsInXml[name]["keypoints"][i*3 + 0] = x
                            annotationsInXml[name]["keypoints"][i*3 + 1] = y
                            annotationsInXml[name]["keypoints"][i*3 + 2] = 1
                            annotationsInXml[name]["num_keypoints"] += 1
                        
                
                 
            else:
                print("File: {} doesn't have any object".format(file))

        else:
            print("File: {} not found".format(file))
            
        for key in annotationsInXml:
            annotations.append(annotationsInXml[key])


    attrDict["images"] = images    
    attrDict["annotations"] = annotations
    attrDict["type"] = "instances"
    jsonString = json.dumps(attrDict,indent=4,sort_keys=True,separators=(",",":"))
    with open("train.json", "w") as f:
        f.write(jsonString)


path="./annotations/"
trainXMLFiles=glob.glob(os.path.join(path, '*.xml'))
XML2JSON(trainXMLFiles)

