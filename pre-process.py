import os
import shutil
import numpy as np
import cv2 

# Define Variables
preproc_dir = "pre-process"
train_dir = "pre-process/train"
val_dir = "pre-process/valid"
test_amt = 0.20
                  
# Create Folder For the Processing          
try: 
    os.mkdir(preproc_dir)
    os.mkdir(train_dir)
    os.mkdir(val_dir)
except:
    print("Directory Exist")
    
#Grab Image Path in directory and move it to new folder format
for path in os.listdir("dataset/"):
    full_path = os.path.join("dataset/",path)
    
    # create dir here
    try: 
        os.mkdir(train_dir+"/"+path)
        os.mkdir(val_dir+"/"+path)
    except:
            print("Directroy exist")
    
    num_im = len(os.listdir(full_path))
    
    for image_path in os.listdir(full_path):
        full_IMpath = full_path+"/"+image_path
        if os.path.isfile(full_IMpath) and np.random.rand(1) < test_amt:
            shutil.copy(full_IMpath,val_dir+"/"+path)
            
        elif os.path.isfile(full_IMpath):
            shutil.copy(full_IMpath,train_dir+"/"+path)
            