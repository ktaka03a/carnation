import os, sys, math, time, random, h5py, time, collections
import numpy as np, pandas as pd, seaborn as sns, tensorflow as tf
from tensorflow import keras
from keras.models import model_from_json
from scipy import stats
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler

def make_dataset(data_length=1000, space_width=5):
    x=pd.Series([random.uniform(-space_width, space_width) for i in range(data_length)], name="x")
    y=pd.Series([random.uniform(-space_width, space_width) for i in range(data_length)], name="y")
    data=pd.concat([x, y], axis=1)
    data.loc[data.x**2+data.y**2<space_width**2/4, "class"]=0
    data.loc[data.x**2+data.y**2>=space_width**2/4, "class"]=1
    x=pd.Series([random.uniform(-space_width, space_width) for i in range(data_length)], name="x")
    y=pd.Series([random.uniform(-space_width, space_width) for i in range(data_length)], name="y")
    testdata=pd.concat([x, y], axis=1)
    data["X1"]=data.x.copy()
    data["X2"]=data.y.copy()
    data.loc[data.x>=space_width/2, "X1"]=space_width/2
    data.loc[data.x<=-space_width/2, "X1"]=-space_width/2
    data.loc[data.y>=space_width/2, "X2"]=space_width/2
    data.loc[data.y<=-space_width/2, "X2"]=-space_width/2
    testdata["X1"]=testdata.x.copy()
    testdata["X2"]=testdata.y.copy()
    testdata.loc[testdata.x>=space_width/2, "X1"]=space_width/2
    testdata.loc[testdata.x<=-space_width/2, "X1"]=-space_width/2
    testdata.loc[testdata.y>=space_width/2, "X2"]=space_width/2
    testdata.loc[testdata.y<=-space_width/2, "X2"]=-space_width/2
    x_train, x_test, y_train, y_test = train_test_split(data.drop(columns=["class"]), data["class"], test_size=0.2, random_state=42)
    rus = RandomUnderSampler(random_state=0)
    x_train, y_train = rus.fit_resample(x_train, y_train)
    x_test, y_test = rus.fit_resample(x_test, y_test)
    return x_train, y_train, x_test, y_test

def flatten(l):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

class weight_file_control:
    name_list=[]
    def __init__(self):
        def append(name):
            self.name_list.append(name)
        self.name_list=[]
        with h5py.File("model_files/weight.hdf5",'r') as f:
            f.visit(append)

    def read(self, form="list"):
        weight_list=[]
        count=0
        data={}
        with h5py.File("model_files/weight.hdf5",'r') as f:
            for name in self.name_list:
                if isinstance(f[name], h5py.Dataset):
                    data[name]=f[name][()]
                    if len(data[name].shape)==1: # bias
                        for x in range(data[name].shape[0]):
                            weight_list.append(data[name][x])
                            count+=1
                    elif len(data[name].shape)==2: # weight
                        for x in range(data[name].shape[0]):
                            for y in range(data[name].shape[1]):
                                weight_list.append(data[name][x][y])
                                count+=1
                    else: #?
                        raise UserWarning("length>3")
        if form=="list":
            return weight_list
        elif form=="dict":
            return data

    def write(self, weight_list):
        count=0
        data={}
        with h5py.File("model_files/weight.hdf5",'r+') as f:
            for name in self.name_list:
                if isinstance(f[name], h5py.Dataset):        
                    data[name]=f[name][()]
            for name in self.name_list:
                if isinstance(f[name], h5py.Dataset):
                    if len(data[name].shape)==1: # bias
                        for x in range(data[name].shape[0]):
                            data[name][x]=weight_list[count]
                            count+=1
                    elif len(data[name].shape)==2: # weight
                        for x in range(data[name][:].shape[0]):
                            for y in range(data[name][:].shape[1]):
                                data[name][:][x][y]=weight_list[count]
                                count+=1
                    else: #?
                        raise UserWarning("length>3")
                    f[name][()]=data[name]

    def read_bias(self, form="list"):
        bias_list=[]
        count=0
        data={}
        with h5py.File("model_files/weight.hdf5",'r') as f:
            for name in self.name_list:
                if isinstance(f[name], h5py.Dataset):
                    data[name]=f[name][()]
                    if len(data[name].shape)==1: # bias
                        for x in range(data[name].shape[0]):
                            bias_list.append(data[name][x])
                            count+=1
        if form=="list":
            return bias_list
        elif form=="dict":
            return data

    def write_bias(self, bias_list):
        count=0
        data={}
        with h5py.File("model_files/weight.hdf5",'r+') as f:
            for name in self.name_list:
                if isinstance(f[name], h5py.Dataset):        
                    data[name]=f[name][()]
            for name in self.name_list:
                if isinstance(f[name], h5py.Dataset):
                    if len(data[name].shape)==1: # bias
                        for x in range(data[name].shape[0]):
                            data[name][x]=bias_list[count]
                            count+=1
                    f[name][()]=data[name]


def read_depth(filetype="info"):
    while True:
        try:
            depth=-pd.read_csv("model_files/depth_{}.csv".format(filetype), header=None)
        except:
            pass
        else:
            break
    return depth