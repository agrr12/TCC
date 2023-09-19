

import analysis_API as AN
import threading
from multiprocessing import Process, Manager
import pandas as pd

path ='CSVs\comparison_metrics\AWARP_hou_w100.csv'
c1 = 'User1'
c2 = 'User2'
# Using the same distance_matrix from before
a = AN.create_comparison_matrix(path, c1, c2, 'AWARP')
df = pd.DataFrame(a)
df.to_csv('matrix.csv')