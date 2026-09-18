import numpy as np


def calculate_mean(values):
    return sum(values) / len(values)


def calculate_max(values):
    return max(values)


def calculate_numpy_statistics(values):
    return {
        "min": np.min(values),
        "max": np.max(values),
        "mean": np.mean(values),
        "std": np.std(values),
    }