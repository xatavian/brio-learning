import numpy as np
from scipy.misc import imresize

def rgb2grey(rgb):
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    grey = 0.2989 * r + 0.5870 * g + 0.1140 * b
    grey = np.expand_dims(grey, axis=2)
    
    return grey

def crop(img,minx,maxx,miny,maxy):
    
    cropImage = img[miny:maxy,minx:maxx]
    
    return cropImage

def preprocessX(img,minx,maxx,miny,maxy):
    res = crop(img,minx,maxx,miny,maxy)
    res = rgb2grey(res)
    
    return res


def shuffleData(imgs_all, anno_all):
    
    c = list(zip(imgs_all, anno_all))
    np.random.shuffle(c)
    imgs_shuffle, anno_shuffle = zip(*c)

    return np.array(imgs_shuffle), np.array(anno_shuffle)


def brightnessAdjust(imgs, brightnessFactor):

    brightFactors = np.swapaxes(np.repeat(np.array([(np.random.rand(len(imgs))-0.5)*brightnessFactor]), 3, axis=0),0,1)

    return np.clip(np.array(list(map(lambda img,num: img+num, imgs, brightFactors))),0,255)

    
    
def flipData(imgs, anno, xmin, xmax, ymin, ymax):  

    imgs_flip = np.concatenate((imgs, np.flip(imgs,1), np.flip(imgs,2), np.flip(np.flip(imgs,1),2)),axis=0)
    
    anno_flip_h = np.ndarray(shape=(imgs.shape[0],2), dtype=float)
    anno_flip_h[:,0] = anno[:,0]
    anno_flip_h[:,1] = (-anno[:,1])+(ymax-ymin)

    anno_flip_v = np.ndarray(shape=(imgs.shape[0],2), dtype=float)
    anno_flip_v[:,0] = (-anno[:,0])+(xmax-xmin)
    anno_flip_v[:,1] = anno[:,1]

    anno_flip_both = np.ndarray(shape=(imgs.shape[0],2), dtype=float)
    anno_flip_both[:,0] = (-anno[:,0])+(xmax-xmin)
    anno_flip_both[:,1] = (-anno[:,1])+(ymax-ymin)

    anno_flip = np.concatenate((anno, anno_flip_h, anno_flip_v, anno_flip_both),axis=0)
    
    return imgs_flip, anno_flip
    
    
def augmentData(imgs, anno, xmin, xmax, ymin, ymax, brightnessFactor, resize = None, color = 'grey'):
    
    # -- Crop the data
    imgs_temp = np.array(list(map(lambda img: crop(img,xmin,xmax,ymin,ymax), imgs)))
    anno_temp = np.array(anno - [xmin, ymin])
    
    # -- Flip the data
    imgs_temp, anno_temp = flipData(imgs_temp, anno_temp, xmin, xmax, ymin, ymax)
    
    # -- Brightness adjust
    imgs_temp = brightnessAdjust(imgs_temp,brightnessFactor)
    #imgs_temp = np.concatenate((imgs_temp, imgs_temp))
    #anno_temp = np.concatenate((anno_temp, anno_temp))
    
    # -- Resize the images 
    if resize:
        imgs_temp = np.array(list(map(lambda img: imresize(img, resize, interp='bilinear', mode=None), imgs_temp)))
    
    # -- Shuffle the data
    imgs_temp, anno_temp = shuffleData(imgs_temp, anno_temp)
    
    if color == 'grey':
        imgs_temp = np.array(list(map(lambda img: rgb2grey(img), imgs_temp)))
    
    return imgs_temp, anno_temp
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    