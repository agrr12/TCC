import import_handle as IH
import requests
import time
from datetime import datetime
import pandas as pd
import os
import matplotlib.pyplot as plt
#62_CNNbrasil
#48_alexandreGarcia
#1_felintoMotoVlog
#2_EDUARDOBOLSONARO

import YT_API_handler as YT
api_key = IH.get_api_key(2)

path = 'C:\\Users\\agrri\PycharmProjects\TCC\project\CSVs\ChannelVideos'
path = 'C:\\Users\\agrri\PycharmProjects\TCC\project\Analysis\HighCommenters\JairBolsonaro\comments_3_JairBolsonaro.csv'



def plot_user_comments_time_series(df):
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['publishedAt'] = df['publishedAt'].dt.strftime('%d-%m-%y')
    autor_id = df.iloc[0]['authorChannelId']

    contagem = df.groupby('publishedAt').size().reset_index(name='COUNT')
    plt.plot(contagem['publishedAt'].to_numpy(),contagem['COUNT'].to_numpy())
    plt.xticks(rotation='vertical')  # Define a rotação das legendas no eixo x
    plt.title(f"Comment Pattern of User {autor_id}")

    output_path = os.path.join('Analysis', 'CommentsTimeSeries')
    IH.create_path_if_not_exists(output_path)

    files = os.listdir(output_path)
    numbers = [int(filename.split('.')[0]) for filename in files if
               filename.endswith('.png') and filename[:-4].isdigit()]
    if numbers:
        highest_number = max(numbers)
    else:
        highest_number = -1
    highest_number+=1
    print(numbers)
    full_output = os.path.join('Analysis', 'CommentsTimeSeries', f"{str(highest_number)}.png")
    plt.savefig(full_output)  # Save the plot to a file
    plt.show()
    return contagem

print(plot_user_comments_time_series(pd.read_csv(path)))
