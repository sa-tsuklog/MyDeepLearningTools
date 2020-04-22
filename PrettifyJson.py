'''
Created on 2020/04/19

@author: sa
'''
import json


IN_FILENAME = "E:/MyDownload/annotations_trainval2017/annotations/person_keypoints_val2017.json"
OUT_FILENAME = "E:/MyDownload/annotations_trainval2017/annotations/person_keypoints_val2017_pret.json"

if __name__ == "__main__":
    with open(IN_FILENAME) as f1:
        data = json.load(f1)
        
        with open(OUT_FILENAME,"w") as f2:
            jsonString = json.dumps(data,indent=4,sort_keys=True,separators=(",",":"))
            f2.write(jsonString)