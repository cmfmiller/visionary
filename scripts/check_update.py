import pandas as pd
import numpy as np


current = pd.read_csv("visionary/data/processed/just_yolo.csv")

print(len(current))
print(current.tail(50))
