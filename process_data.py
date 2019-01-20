from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
import numpy as np


def scale_data(data):
    data = np.array(data).reshape(-1,1)
    scaler = joblib.load('C:/Users/Adrian/Desktop/Hackathons/Swamp/scaler.save')
    return scaler.transform(data)


def make_windows(data, size):
    X = []
    i = 0
    while(i+size) <= len(data)-1:
        X.append(data[i:i+size])
        i += 1

    return X

def prep_for_model(data, timesteps, features):
    return np.array(data).reshape(len(data), timesteps, features)
