'''
Created on 2020/04/03

@author: sa
'''

import glob
import os
import cv2
import random
from libs.pascal_voc_io import PascalVocReader,PascalVocWriter


IN_DIR = "F:/dataset/4K/"
TRAIN_OUT_DIR = "F:/dataset/train/"
VALID_OUT_DIR = "F:/dataset/valid/"

PX_OUTSIZE = 512
PX_MINSIZE = 20
PX_MAXSIZE = 490
MIN_SCALE = 0.01
ARGUMENTATION = 10
TRAIN_RATIO = 0.8

def scaleAndOffset(src, xmin,ymin,xmax,ymax,outPath,className):
    width = xmax-xmin
    height = ymax-ymin
    #######################
    # scale
    #######################
    
    scale = random.uniform(MIN_SCALE,1.0)
    
    
    if((width*scale < PX_MINSIZE) and (height*scale < PX_MINSIZE)):
        scale = PX_MINSIZE/width if (PX_MINSIZE/width < PX_MINSIZE/height) else PX_MINSIZE/height
    
    if((width*scale > PX_MAXSIZE) or (height*scale > PX_MAXSIZE)):
        scale = PX_MAXSIZE/width if (PX_MAXSIZE/width < PX_MAXSIZE/height) else PX_MAXSIZE/height
    
    if(src.shape[1]*scale < PX_OUTSIZE or src.shape[0]*scale < PX_OUTSIZE):
        scale = PX_OUTSIZE/src.shape[1] if(src.shape[1]<src.shape[0]) else PX_OUTSIZE/src.shape[0]
    
    if(scale > 1.0):
        scale = 1.0
    
    
    dst = cv2.resize(src,dsize=None,fx=scale,fy=scale)
    
    #######################
    # offset
    #######################
    offsetX = (PX_OUTSIZE - width*scale)/2 * random.uniform(-1.0,1.0)
    offsetY = (PX_OUTSIZE - height*scale)/2 * random.uniform(-1.0,1.0)
    
    
    left = int((xmin+width/2)*scale-PX_OUTSIZE/2+offsetX)
    top  = int((ymin+height/2)*scale-PX_OUTSIZE/2+offsetY)
    
    if(left<0):
        offsetX -= left
        left = 0
     
    if(left+PX_OUTSIZE > dst.shape[1]):
        offsetX -= left-(dst.shape[1]-PX_OUTSIZE) 
        left = dst.shape[1]-PX_OUTSIZE
         
    if(top<0):
        offsetY -= top
        top = 0
     
    if(top+PX_OUTSIZE > dst.shape[0]):
        offsetY -= top-(dst.shape[0]-PX_OUTSIZE) 
        top = dst.shape[0]-PX_OUTSIZE
        
    
    dst = dst[top:top+PX_OUTSIZE,left:left+PX_OUTSIZE]
    
    outXmin = int(PX_OUTSIZE/2-width*scale/2-offsetX)
    outYmin = int(PX_OUTSIZE/2-height*scale/2-offsetY)
    outXmax = int(PX_OUTSIZE/2+width*scale/2-offsetX)
    outYmax = int(PX_OUTSIZE/2+height*scale/2-offsetY)
    
    
    cv2.imwrite(outPath,dst)
    
    foldername = os.path.basename(os.path.dirname(outPath))
    filename = os.path.basename(outPath)
    imgSize = (PX_OUTSIZE,PX_OUTSIZE)
    
    xmlWriter = PascalVocWriter(foldername,filename,imgSize,localImgPath=outPath)
    xmlWriter.addBndBox(outXmin,outYmin,outXmax,outYmax,className,0)
    xmlWriter.save(outPath[:-4]+".xml")
    
#     cv2.rectangle(dst,(outXmin,outYmin),(outXmax,outYmax),(255,0,0))
#      
#     print("------------")
#     print("shape",dst.shape)
#      
#     print("top",top)
#     print("left",left)
#      
#      
#     print("scale:",scale)
#     print("width:",width*scale)
#     print("height:",height*scale)
#     print("xMin:",outXmin)
#     print("yMin:",outYmin)
#     print("xMax:",outXmax)
#     print("yMax:",outYmax)
#      
#     cv2.imshow("preview",dst)
#     c = cv2.waitKey(0)

if __name__ == "__main__":
    random.seed(1)
    
    filenames = sorted(glob.glob(IN_DIR+"/**/*.png"))
    
    
    count = 0
    
    for filename in filenames:
        xmlName = filename[:-4]+".xml"
        basename = os.path.basename(filename)
        dirname = os.path.basename(os.path.dirname(filename))
        
        if(not os.path.exists(TRAIN_OUT_DIR+dirname)):
            os.makedirs(TRAIN_OUT_DIR+dirname)
        if(not os.path.exists(VALID_OUT_DIR+dirname)):
            os.makedirs(VALID_OUT_DIR+dirname)
        
        src = cv2.imread(filename)
        xmlReader = PascalVocReader(xmlName)
        shapes = xmlReader.getShapes()
        
        xmin = shapes[0][1][0][0]
        ymin = shapes[0][1][0][1]
        xmax = shapes[0][1][2][0]
        ymax = shapes[0][1][2][1]
        className = shapes[0][0]
        #className = "aircraft"
        
        print(dirname)
        print(basename)
        
        if(random.uniform(0.0,1.0) < TRAIN_RATIO):
            for i in range(ARGUMENTATION):
                scaleAndOffset(src, xmin, ymin, xmax, ymax, TRAIN_OUT_DIR+dirname+"/"+basename[:-4]+"_"+str(i)+".jpg",className)
        else:    
            scaleAndOffset(src, xmin, ymin, xmax, ymax, VALID_OUT_DIR+dirname+"/"+basename[:-4]+".jpg",className)
        
#         count+=1
#         if(count > 20):
#             break
        