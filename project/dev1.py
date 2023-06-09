import json
import time
from datetime import datetime
import analysis_API as AN

import requests
import pandas as pd
import import_handle as IH
import YT_API_handler as YT
import os



#playlist_id = 'UUk5BcU1rOy6hepflk7_q_Pw'
#df = pd.read_csv('CSVs/channels_info.csv')


folder_path = 'CSVs\Comments\JovemPanNews'  # Replace with the actual folder path





AN.find_high_frequency_commenter(folder_path)