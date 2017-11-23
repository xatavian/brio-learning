import os
from os import listdir
from os.path import isfile, join
from scipy import misc 
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input
from keras.models import Model

import matplotlib.pyplot as plt
import matplotlib

import numpy as np

try:
    print("Dectecting IPython...")
    __IPYTHON__
    get_ipython().magic('matplotlib inline')
    print("Matplotlib is configured to use ", plt.get_backend())
except:
    print("IPython was not detected. No GUI backend was set up for matplotlib.")
    print("No graph will be shown.")
    
def load_dataset(filename, path, windows=False, verbose=False, preprocess=None, **args):
    """
    Reads a dataset file and loads the images.
    If needed, the images can be preprocessed before being saved.
    """
    raws, imgs, coords = [], [], []
    windows = args.pop("windows", False)
    verbose = args.pop("verbose", False)
    
    with open(filename,"r") as file:
        for line in file:
            imgFile, x, y = line.split(" ")
            
            if windows: imgFile.replace('/',"\\")
            if verbose: print("Loading ", imgFile)
            
            img = image.load_img(os.path.join(path, imgFile), **args)
            img = image.img_to_array(img)
            #img = np.expand_dims(img, axis=0)
            raw = misc.imread(os.path.join(path, imgFile))
            if preprocess:
                img = preprocess(img.copy())
            
            imgs.append(img)
            raws.append(raw)
            coords.append((int(x), int(y)) )

    return np.array(raws), np.array(imgs), np.array(coords)

def load_data_list(path, fileList, windows=False, verbose=False, preprocess=None, **args):
    """
    Reads a data folder and loads the images.
    If needed, the images can be preprocessed before being saved.
    """
    raws, imgs, coords = [], [], []
    
    
    for datasetFile in fileList:

        windows = args.pop("windows", False)
        verbose = args.pop("verbose", False)
        with open(datasetFile,"r") as file:
            for line in file:
                imgFile, x, y = line.split(" ")

                if windows: imgFile.replace('/',"\\")
                if verbose: print("Loading ", imgFile)

                img = image.load_img(os.path.join(path, imgFile), **args)
                img = image.img_to_array(img)
                #img = np.expand_dims(img, axis=0)
                raw = misc.imread(os.path.join(path, imgFile))
                if preprocess:
                    img = preprocess(img.copy())

                imgs.append(img)
                raws.append(raw)
                coords.append((int(x), int(y)) )

    return np.array(raws), np.array(imgs), np.array(coords)



def plot_result(image, predicted_position, expected_position, title=""):
    """
    Plots an image with the predicted position as well as with the
    expected position.
    """
    label = "Predicted output: ({}, {})".format(
            int(predicted_position[0]), 
            int(predicted_position[1])
    )
    expected_label = "Expected output ({}, {})".format(
            int(expected_position[0]),
            int(expected_position[1])
    )
        
    fig = plt.figure()
    
    ax = fig.add_subplot(111, title = title)
    ax.imshow(image)
    ax.scatter(predicted_position[0], 
               predicted_position[1], 
               c="r", label=label)
    ax.scatter(expected_position[0],
               expected_position[1],
               c="r", marker="x", label=expected_label)
    
    ax.legend(bbox_to_anchor=(1,1))
    return fig, ax

    
def visLayer(aImg, aModel, layerNo, filterNo):
    
    model = Model(inputs = aModel.input, outputs = aModel.layers[layerNo].output)
    img = model.predict(np.expand_dims(aImg, axis=0))
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111, title = aModel.layers[layerNo].name)
    ax.imshow(img[0,:,:,filterNo], cmap='gray')
    
    return fig, ax

def selectiveWeights(model_base, layer, filters, filtersPrev):

    weights = model.layers[layer].get_weights()[0][:,:,:,filters][:,:,filtersPrev,:]
    biases = model.layers[layer].get_weights()[1][filters]
    newWeights = [weights, biases]

    return newWeights








#x, y = load_dataset('Annotated Datasets/whole_white_fromCenter.txt', "Annotated Datasets/")
#print(x)
#print(y)