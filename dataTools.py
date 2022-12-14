import torch
import torch.nn.functional as F
from torch.utils.data import  Dataset 
from torchvision import transforms, utils
import matplotlib.pyplot as plt

import numpy as np
import os
from PIL import Image
#######################################################################
########### Main dataset classes ######################################
class imgRead_fromList(Dataset):
    """
    Reads and pre-processes images from a text file of names.
    """

    def __init__(self, root, img_names_list, img_size, transform=None):
        """
        Assumes that self.img_names_list is a text-file listing all the images relevant to
        this class (already split to train-valid-test). Every line of self.img_names_list, 
        pre-pended with self.root, constructs an absolute address to an image in 
        your disk.
        self.img_size is (C, H, W).
        self.transform is the desired optional pre-processing. 
        ** Note that torchvision.transform.ToTensor() is always applied by defalut.**
        """

        self.root = root
        self.img_names_list = img_names_list
        self.img_size = img_size
        self.transform = transform

    def __len__(self):
        return len(self.img_names_list)

    def __getitem__(self, idx):
        '''with open(self.img_names_list) as f:
            img_name = f.readlines()[idx][:-1]'''
            
        img_name = self.img_names_list[idx]
        img_path = os.path.join(self.root, img_name)
        
        img = Image.open(img_path)
        img = img.resize(self.img_size[1:], Image.ANTIALIAS)

        sample = {}
        sample['name'] = img_name
        if self.transform:
             img = self.transform(img)
            
        sample['image'] = transforms.ToTensor()(img)

        return sample

#######################################################################
class imgRead_fromDir(Dataset): 
    """
    Reads and pre-processes images from a root directory.
    """
    def __init__(self, root, img_size, transform=None):
        """
        Assumes that self.root is flat directory containing the relevant images to be 
        loaded by this class. So use it when you have explicit train-valid-test devisions
        each as a separate directory.
        self.img_size is (C, H, W).
        self.transform is the desired optional pre-processing. 
        ** Note that torchvision.transform.ToTensor() is always applied by defalut.**
        """
        self.root = root
        self.img_size = img_size
        self.transform = transform
        self.image_names = os.listdir(root)

    def __len__(self):
        return int(len(os.listdir(self.root)))

    def __getitem__(self, idx):
        img_name = os.listdir(self.root)[idx]
        img_path = os.path.join(self.root, img_name)
        
        img = Image.open(img_path)
        img = img.resize(self.img_size[1:], Image.ANTIALIAS)

        sample = {}
        sample['name'] = img_name
        if self.transform:
             img = self.transform(img)
            
        sample['image'] = transforms.ToTensor()(img)

        return sample

########################################################
############ Some handy function #######################
def pathStamper(path, now, append=None):
    """
    Stamps the input path with the time-stamp of the current moment.
    """
    path_stmp = os.path.splitext(path)[0] + '_stmp'
    path_stmp +=  now
    if append is not None:
        path_stmp += append
    path_stmp += os.path.splitext(path)[1]
    return  path_stmp
##################################################
def list2str(L):
    """
    A function useful for relevant naming of networks w.r.t. their list of parameters.
    """
    s = ''
    for i,l in enumerate(L):
        s += str(l)
        if i < len(L) - 1:
            s += '-'
    return s   

#################### Plot tools ########################################################
def imShow(img, idx=0):
    """
    A handy function to show images from PyTorch tensors or numpy arrays.
    
    Accepts tensors/arrays with 4 axes (batch, channel, height, weight) or 
    3 axes (channel, height, weight). Select the desired instance with idx.
    """
    if isinstance(img, np.ndarray):
        if len(img.shape) == 4:
            (_, c, h, w) = img.shape
            img = img[idx, :, :, :].reshape(c, h, w)
        
    if isinstance(img, torch.Tensor):
        if len(img.shape) == 4:
            (_, c, h, w) = img.shape
            img = img[idx, :, :, :].detach().squeeze(0).cpu().view(c, h, w).numpy()
            print(img.shape)
        else:
            (c, h, w) = img.shape
            print(img.shape)
            img = img.detach().cpu().view(c, h, w).numpy()
            print(img.shape)

    plt.figure()    
    if c == 3:
        plt.imshow(np.transpose(img, (1, 2, 0)), interpolation='nearest')
    elif c == 1:
        plt.imshow(img[0,:,:], interpolation='nearest')
    plt.show()     
