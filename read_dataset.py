import os
from scipy import misc 

def load_dataset(filename, path, **args):
    dataset = []
    with open(filename,"r") as file:
        for line in file:
            imgFile, x, y = line.split(" ")
            img = misc.imread(os.path.join(path, imgFile), **args)
            dataset.append([img, (int(x), int(y))])
    
    return dataset            
