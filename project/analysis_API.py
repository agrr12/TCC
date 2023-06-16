import os
import pandas as pd
import import_handle as IH
import matplotlib.pyplot as plt

def find_high_frequency_commenter(comment_folder_path):
    """
    Finds high-frequency commenters from a folder containing comment files.

    Args:
        comment_folder_path (str): The path to the folder containing the comment files.

    Returns:
        None

    This function iterates over all files in the specified folder, reads the comment files into DataFrames,
    and combines them into a single DataFrame. It then counts the number of comments per unique authorChannelId,
    identifies high-frequency commenters (those with a count of 40 or more), sorts them in descending order based
    on the comment count, and saves the result to a file. Additionally, for each high-frequency commenter, it
    creates a separate DataFrame containing their comments and saves it to a specific folder.

    The function relies on the 'os' and 'pandas' libraries and assumes that the comment files are in CSV format.
    """
    df_list = []
    # Iterate over all files in the folder
    for file_name in os.listdir(comment_folder_path):
        if os.path.isfile(os.path.join(comment_folder_path, file_name)):
            df = pd.read_csv(os.path.join(comment_folder_path, file_name))
            df_list.append(df)
    if df_list == []:
        return
    channel = os.listdir(comment_folder_path)[0].split(("_"))[2].replace(".csv", "")
    df_final = pd.concat(df_list)
    df_count_posts = df_final.groupby('authorChannelId').size().reset_index(name='Count')
    df_high_commenters = df_count_posts[df_count_posts['Count'] >=40]
    df_high_commenters_sorted = df_high_commenters.sort_values(by='Count', ascending=False)
    IH.save_df('Analysis', f"High_Commenters_{channel}", 'w', df_high_commenters_sorted, add_time=False)
    count = 0
    for _,row in df_high_commenters_sorted.iterrows():
        df_high_commenter = df_final[df_final['authorChannelId'] == row['authorChannelId']]
        path = os.path.join('Analysis','HighCommenters',channel)
        file_name = f"comments_{str(count)}_{channel}"
        IH.save_df(path, file_name, 'w', df_high_commenter, add_time=False)
        count+=1

def plot_user_comments_time_series(df, channel):
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['publishedAt'] = df['publishedAt'].dt.strftime('%d-%m-%y')
    autor_id = df.iloc[0]['authorChannelId']

    contagem = df.groupby('publishedAt').size().reset_index(name='COUNT')
    # Create a DataFrame for all days of a month, in this case, October 2022
    all_dates = pd.DataFrame({
        'publishedAt': pd.date_range(start='2022-10-01', end='2022-11-01')
    })

    # Convert the 'publishedAt' column to datetime, if it's not already
    contagem['publishedAt'] = pd.to_datetime(contagem['publishedAt'])

    # Merge the two DataFrames
    contagem = pd.merge(all_dates, contagem, on='publishedAt', how='left')

    # Fill NaN values in 'COUNT' with zero
    contagem['COUNT'] = contagem['COUNT'].fillna(0)

    plt.plot(contagem['publishedAt'].to_numpy(),contagem['COUNT'].to_numpy())


    plt.xticks(rotation='vertical')  # Define a rotação das legendas no eixo x
    plt.title(f" User {autor_id} on {channel}")
    plt.ylim(0, 50)

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
    #print(numbers)
    plt.tight_layout()
    full_output = os.path.join('Analysis', 'CommentsTimeSeries', f"{str(highest_number)}.png")
    plt.savefig(full_output)  # Save the plot to a file
    plt.close()
    #plt.show()
    return contagem
