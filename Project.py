import zipfile

from PIL import Image
from PIL import ImageDraw
import pytesseract
import cv2 as cv
import numpy as np
import pytesseract
from kraken import pageseg
import math

face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

def zip_images_extraction(name):
    zip_name = 'readonly/' + name
    out = []
    
    with zipfile.ZipFile(zip_name) as myzip:
        zip_infos = myzip.infolist()
        
        for ele in zip_infos:
            name = ele.filename
            img = Image.open(myzip.open(name))
            img_strs = pytesseract.image_to_string(img.convert('L'))
            
            if ("Christopher" in img_strs) or ("Mark" in img_strs):
                my_dic = {"name":name, "img":img, "text":img_strs}
                out.append(my_dic)
    return out          

small_imgs = zip_images_extraction("small_img.zip")
big_imgs = zip_images_extraction("images.zip")

def extract_faces(img, scale_factor):
    gray = np.array(img.convert("L"))
    faces = face_cascade.detectMultiScale(gray, scale_factor)
    
    if (len(faces) == 0):
        return None
    
    faces_imgs = []
    
    for x,y,w,h in faces:
        faces_imgs.append(img.crop((x,y,x+w,y+h)))
    
    ncols = 5
    nrows = math.ceil(len(faces) / ncols)
    
    contact_sheet=Image.new(img.mode, (550, 110*nrows))
    x, y = (0, 0)
    
    for face in faces_imgs:
        face.thumbnail((110,110))
        contact_sheet.paste(face, (x,y))
        
        if x+110 == contact_sheet.width:
            x = 0
            y += 110
        else:
            x += 110
            
    return contact_sheet

def value_search(value, zip_name, scale_factor):
    if zip_name == "small_img.zip":
        ref_imgs = small_imgs
    else:
        ref_imgs = big_imgs
    
    for ele in ref_imgs:
        if value in ele["text"]:
            print("Results found in file {}".format(ele["name"]))
            img = ele["img"]
            contact_sheet = extract_faces(img, scale_factor)
            if contact_sheet is not None:
                display(contact_sheet)
            else:
                print("But there were no faces in that file")
                
value = "Christopher"
zip_name = "small_img.zip"

value_search(value, zip_name, scale_factor = 1.4)
value_search(value = "Mark", zip_name = "images.zip", scale_factor = 1.4)
