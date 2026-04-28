# plots/utils.py

def symmetric_limits(data):
    m = max(abs(data.min()), abs(data.max()))
    return -m, m
