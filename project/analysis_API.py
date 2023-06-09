import os
import pandas as pd
import import_handle as IH

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
