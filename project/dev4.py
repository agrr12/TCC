

import analysis_API as AN
import threading
from multiprocessing import Process, Manager
import pandas as pd

import os

if __name__ == '__main__':
    manager = Manager()
    shared_list = manager.list()
    df = pd.read_csv('/home/agrr/ProjectsPy/TCC/encoded_seconds.csv')[1:100]
    AN.run_awarp_on_csv_parallel(df, 'encode_sec', 't.csv', shared_list)