

import analysis_API as AN
import threading
from multiprocessing import Process, Manager
import pandas as pd

import os
#3
if __name__ == '__main__':
    processes = 16

    df = pd.read_csv('/TCC/project/CSVs/encoded_TS/encoded_hours.csv').to_numpy()
    AN.run_awarp_on_csv_parallel(df, 'AWARP_hou_w100.csv', processes)

    #df = pd.read_csv('/home/agrr/ProjectsPy/TCC/encoded_minutes.csv').to_numpy()
    #AN.run_awarp_on_csv_parallel(df, 'encode_min', 'AWARP_min_w100.csv', processes)

    #df = pd.read_csv('/home/agrr/ProjectsPy/TCC/encoded_seconds.csv').to_numpy()
    #AN.run_awarp_on_csv_parallel(df, 'encode_sec', 'AWARP_sec_w100.csv', processes)