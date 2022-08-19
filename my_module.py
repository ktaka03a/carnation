import os, sys, math, time, random, h5py, time
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



