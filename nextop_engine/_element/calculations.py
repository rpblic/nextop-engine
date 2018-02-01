import numpy as np


def rmse(a, b):
    sum = 0
    for i in range(len(a)):
        sum = sum + (a[i] - b[i]) ** 2
    return np.sqrt(sum / len(a))


def map_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def map_error_with_std(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    std_arr= np.std(y_true- y_pred)
    return np.mean(np.abs((y_true - y_pred + std_arr) / (y_true + std_arr))) * 100


def map_error_div_std(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    std_arr= np.std(y_true- y_pred)
    return np.mean(np.abs((y_true - y_pred) / std_arr)) * 100


def smap_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return (np.sum(np.abs(y_true - y_pred)) / np.sum(y_true + y_pred)) * 2 * 100


def rms_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.sqrt(((y_true - y_pred)**2).mean(axis=None))


def minMaxNormalizer(data):
    numerator = data - np.min(data)
    denominator = np.max(data) - np.min(data)
    return numerator / (denominator + 1e-7)


def minMaxDeNormalizer(data, originalData):
    shift = np.min(originalData)
    multiplier = np.max(originalData) - np.min(originalData)
    return (data + shift) * multiplier
