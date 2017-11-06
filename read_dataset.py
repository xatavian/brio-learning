import os
from scipy import misc 
import numpy as np

def load_dataset(filename, path, **args):
    dataset = []
    
    windows = args.pop("windows", False)
    
    with open(filename,"r") as file:
        for line in file:
            imgFile, x, y = line.split(" ")
            
            if windows: imgFile.replace('/',"\\")
               
            print("Loading ", imgFile)
            
            img = misc.imread(os.path.join(path, imgFile), **args)
            dataset.append([img, (int(x), int(y))])

    imgs, coords = [], []
    for img, coord in dataset:
        imgs.append(img)
        coords.append(coord)
        
    return np.array(imgs), np.array(coords)