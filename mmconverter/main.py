import csv
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np

from mmconverter.params import ROW_OFFSET, HOME
from mmconverter.utils import *

if __name__ == "__main__":
    
    path_to_file = os.path.join(sys.argv[1])
    print(path_to_file)

    rows = load_file(filename = path_to_file)
    df = process_rows(rows)

    print(df.head())

    export_csv(df, path_to_file)
    print("The file was successfully converted.")

    

