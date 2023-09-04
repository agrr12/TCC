import os
import pandas as pd
import import_handle as IH
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from skimage.metrics import structural_similarity as ssim, peak_signal_noise_ratio as psnr
import warnings
import pickle

def compare_images(directory, output_directory):
    """
    Compares all pairs of images in the provided directory using several metrics:
    Mean Squared Error (MSE), Normalized Root Mean Square Error (NRMSE),
    Structural Similarity Index (SSIM), and Peak Signal-to-Noise Ratio (PSNR).
    The results are then saved as CSV files in the specified output directory.

    Parameters:
    - directory (str): The path to the directory containing the images to be compared.
                       Images should be in .png format.
    - output_directory (str): The path to the directory where the CSV files with
                              comparison results will be saved.

    CSV Outputs:
    - mse_comparison.csv: Contains the MSE values for each pair of images.
    - nrmse_comparison.csv: Contains the NRMSE values for each pair of images.
    - ssim_comparison.csv: Contains the SSIM values for each pair of images.
    - psnr_comparison.csv: Contains the PSNR values for each pair of images.

    Returns:
    None
    """
    warnings.simplefilter(action='ignore', category=FutureWarning)

    df_mse = pd.DataFrame(columns=['Image1', 'Image2', 'MSE'])
    df_nrmse = pd.DataFrame(columns=['Image1', 'Image2', 'NRMSE'])
    df_ssim = pd.DataFrame(columns=['Image1', 'Image2', 'SSIM'])
    df_psnr = pd.DataFrame(columns=['Image1', 'Image2', 'PSNR'])

    images = [f for f in os.listdir(directory) if f.endswith('.png')]

    for i in range(len(images)):
        for j in range(i+1, len(images)):
            print(i, j)
            img1_path = os.path.join(directory, images[i])
            img2_path = os.path.join(directory, images[j])

            image1 = cv2.imread(img1_path)
            image2 = cv2.imread(img2_path)

            # ensure the two images have the same dimensions
            image1_resized = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

            mse = np.mean((image1_resized - image2) ** 2)
            max_value = np.max(image1_resized)
            nrmse = np.sqrt(mse) / max_value
            ssim_val = ssim(image1_resized, image2, multichannel=True)
            psnr_val = psnr(image1_resized, image2, data_range=max_value)

            df_mse = pd.concat([df_mse, pd.DataFrame([{'Image1': images[i], 'Image2': images[j], 'MSE': mse}])], ignore_index=True)
            df_nrmse = pd.concat([df_nrmse, pd.DataFrame([{'Image1': images[i], 'Image2': images[j], 'NRMSE': nrmse}])], ignore_index=True)
            df_ssim = pd.concat([df_ssim, pd.DataFrame([{'Image1': images[i], 'Image2': images[j], 'SSIM': ssim_val}])], ignore_index=True)
            df_psnr = pd.concat([df_psnr, pd.DataFrame([{'Image1': images[i], 'Image2': images[j], 'PSNR': psnr_val}])], ignore_index=True)

    df_mse.to_csv(os.path.join(output_directory, 'mse_comparison.csv'), index=False)
    df_nrmse.to_csv(os.path.join(output_directory, 'nrmse_comparison.csv'), index=False)
    df_ssim.to_csv(os.path.join(output_directory, 'ssim_comparison.csv'), index=False)
    df_psnr.to_csv(os.path.join(output_directory, 'psnr_comparison.csv'), index=False)

def ConstrainedAWARP(x, y, w):
    """
    Computes the Constrained Adaptive Weighted Asymmetric Time Warping (AWARP)
    distance between two sequences, x and y, with a given window size w. This function
    takes into account the timestamps of events in both sequences and returns the
    computed distance as well as a matrix detailing the warping costs between points.

    Parameters:
    - x (list of int): The first input sequence of events, represented as a list of integers.
                       Positive values indicate the number of events, while negative values
                       denote waiting times (gaps) between events.
    - y (list of int): The second input sequence, structured similarly to x.
    - w (int): Window size that constrains the warping. Events farther apart than this window
               will not be matched.

    Returns:
    - d (float): The square root of the AWARP distance between the two sequences.
    - D (2D numpy array): A matrix detailing the warping costs between points in the two sequences.
    """
    # Make copies of the input lists so as to not modify the originals
    x = x[:]
    y = y[:]

    # Initialize the lengths of both sequences and append the value '1' to each.
    n = len(x)
    m = len(y)
    x.append(1)
    y.append(1)

    # Convert lists to numpy arrays for efficient calculations
    x = np.array(x)
    y = np.array(y)

    # Create a 2D array filled with infinity for dynamic programming.
    D = np.inf * np.ones((n+1, m+1))
    D[0][0] = 0  # Base case

    # Calculate the timestamps of the events in x.
    tx = np.zeros(n+1, dtype=int)
    iit = 0
    for i in range(n+1):
        if x[i] > 0:
            iit += 1
            tx[i] = iit
        else:
            iit += abs(x[i])
            tx[i] = iit

    # Similarly, calculate the timestamps of the events in y.
    ty = np.zeros(m+1, dtype=int)
    iit = 0
    for i in range(m+1):
        if y[i] > 0:
            iit += 1
            ty[i] = iit
        else:
            iit += abs(y[i])
            ty[i] = iit

    # Iterate through both sequences to compute the warping cost.
    for i in range(n):
        for j in range(m):
            gap = abs(tx[i] - ty[j])

            # If the gap between events is larger than w, set to infinity.
            if gap > w and ((j > 0 and ty[j-1] - tx[i] > w) or (i > 0 and tx[i-1] - ty[j] > w)):
                D[i+1][j+1] = np.inf
            else:
                # Initialize three possible costs (from diagonal, left, and top).
                a1, a2, a3 = np.inf, np.inf, np.inf

                # Cost calculation for matching x[i] and y[j].
                if x[i] > 0 and y[j] > 0 and gap <= w:
                    a1 = D[i][j] + (x[i] - y[j]) ** 2
                elif x[i] < 0 and y[j] < 0:
                    a1 = D[i][j]
                elif x[i] > 0 and y[j] < 0:
                    a1 = D[i][j] + x[i] ** 2 * (-y[j])
                elif x[i] < 0 and y[j] > 0:
                    a1 = D[i][j] + y[j] ** 2 * (-x[i])

                # Cost calculation for matching x[i] and a gap in y.
                if x[i] > 0 and y[j] > 0 and gap <= w:
                    a2 = D[i+1][j] + (x[i] - y[j]) ** 2
                elif x[i] < 0 and y[j] < 0:
                    a2 = D[i+1][j]
                elif x[i] < 0 and y[j] > 0:
                    a2 = D[i+1][j] + y[j] ** 2
                elif x[i] > 0 and y[j] < 0 and gap <= w:
                    a2 = D[i+1][j] + x[i] ** 2 * (-y[j])

                # Cost calculation for matching y[j] and a gap in x.
                if x[i] > 0 and y[j] > 0 and gap <= w:
                    a3 = D[i][j+1] + (x[i] - y[j]) ** 2
                elif x[i] < 0 and y[j] < 0:
                    a3 = D[i][j+1]
                elif x[i] > 0 and y[j] < 0:
                    a3 = D[i][j+1] + x[i] ** 2
                elif x[i] < 0 and y[j] > 0 and gap <= w:
                    a3 = D[i][j+1] + y[j] ** 2 * (-x[i])

                # Store the minimum of the three computed costs.
                D[i+1][j+1] = min([a1, a2, a3])

    # Return the square root of the final cell value as the distance and the matrix D.
    d = np.sqrt(D[n][m])
    return d, D

def AWARP(x, y):
    """
    Compute the Adaptive Weighted Asymmetric Time Warping (AWARP) distance between two sequences x and y.
    This function calculates the warping cost between points without any constraining window.

    Parameters:
    - x (list of int): The first input sequence represented as a list of integers where positive
                       values denote events and negative values indicate the length of runs of zeros (gaps).
    - y (list of int): The second input sequence, structured similarly to x.

    Returns:
    - d (float): The square root of the AWARP distance between the two sequences.
    - D (2D numpy array): A matrix detailing the warping costs between points in the two sequences.

    Note:
    Both input sequences are treated as run-length encoded, where positive integers represent events
    and negative integers represent the length of runs of zeros.
    """
    # Create copies of the input lists to ensure original lists are not modified
    x = x[:]
    y = y[:]

    # x and y are run-length encoded series where negative integers represent
    # length of runs of zeros
    n = len(x)
    m = len(y)

    x.append(1)
    y.append(1)

    # Convert lists to numpy arrays for efficient calculations
    x = np.array(x)
    y = np.array(y)

    # Initializing matrix D with infinities and setting D[0][0] to 0
    D = np.full((n+1, m+1), np.inf)
    D[0, 0] = 0

    for i in range(n):
        for j in range(m):
            a1 = D[i, j] + (x[i] - y[j]) ** 2

            if i > 0 and j > 0:
                conditions = [
                    (x[i] > 0 and y[j] > 0),
                    (x[i] < 0 and y[j] < 0),
                    (x[i] > 0 and y[j] < 0),
                    (x[i] < 0 and y[j] > 0)
                ]

                values = [
                    D[i, j] + (x[i] - y[j]) ** 2,
                    D[i, j],
                    D[i, j] + x[i] ** 2 * (-y[j]),
                    D[i, j] + y[j] ** 2 * (-x[i])
                ]

                a1 = np.select(conditions, values, default=np.inf)

            conditions = [
                (x[i] > 0 and y[j] > 0),
                (x[i] < 0 and y[j] < 0),
                (x[i] < 0 and y[j] > 0),
                (x[i] > 0 and y[j] < 0)
            ]

            values = [
                D[i+1, j] + (x[i] - y[j]) ** 2,
                D[i+1, j],
                D[i+1, j] + y[j] ** 2,
                D[i+1, j] + x[i] ** 2 * (-y[j])
            ]

            a2 = np.select(conditions, values, default=np.inf)

            conditions = [
                (x[i] > 0 and y[j] > 0),
                (x[i] < 0 and y[j] < 0),
                (x[i] > 0 and y[j] < 0),
                (x[i] < 0 and y[j] > 0)
            ]

            values = [
                D[i, j+1] + (x[i] - y[j]) ** 2,
                D[i, j+1],
                D[i, j+1] + x[i] ** 2,
                D[i, j+1] + y[j] ** 2 * (-x[i])
            ]

            a3 = np.select(conditions, values, default=np.inf)

            D[i+1, j+1] = min([a1, a2, a3])

    d = np.sqrt(D[n, m])
    return d, D

def run_awarp_on_csv(pd_df, column_name, awarp_or_cawarp, output_name):
    """
    Reads a CSV file, processes its data, computes the AWARP distance for each pair of series,
    and saves the result in another CSV file.

    :param pd_df: Pandas dataframe.
    :param column_name: Name of the column that contains the series data.
    :param output_name: Name of the output CSV file.
    """
    results_df = pd.DataFrame(columns=['id1', 'id2', 'result'])

    for x1, y1 in pd_df.iterrows():
        print(column_name[:3], x1)
        id1 = y1['authorChannelId']
        series1 = [int(i) for i in y1[column_name].strip('[]').split(',')]
        for x2, y2 in pd_df[int(x1) + 1:].iterrows():
            id2 = y2['authorChannelId']
            series2 = [int(i) for i in y2[column_name].strip('[]').split(',')]
            result = ConstrainedAWARP(series1, series2, 100)[0] if awarp_or_cawarp.lower() == 'awarp' else AWARP(series1, series2)
            # Append the results to the new dataframe
            results_df.loc[len(results_df)] = [id1, id2, result]

    results_df.to_csv(output_name, index=False)

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

def unify_dataframes(p, columns):
    """
    Unifies data from CSV files within subdirectories of a given directory
    into a single DataFrame based on the specified columns.

    :param p: Root directory containing subdirectories with CSV files.
    :param columns: List of column names to extract from the CSVs.
    :return: Unified DataFrame containing specified columns from all CSVs.
    """

    all_data = []  # List to collect data from each CSV file

    for x in os.listdir(p):
        for y in os.listdir(os.path.join(p, x)):
            file_path = os.path.join(p, x, y)
            df = pd.read_csv(file_path, usecols=columns)
            all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    unified_df = pd.concat(all_data, ignore_index=True)

    return unified_df

def create_comparison_matrix(input_file='CAWARP_results_hours_100.csv', pickle_output_file='matrix.pkl'):
    """
    Create a symmetric matrix based on the given input CSV file and save it to the specified Pickle file.

    Parameters:
    - input_file (str): Path to the input CSV file. Defaults to 'CAWARP_results_hours_100.csv'.
    - pickle_output_file (str): Path to save the matrix as a Pickle file. Defaults to 'matrix.pkl'.

    Returns:
    - DataFrame: The resulting matrix.
    """
    df = pd.read_csv(input_file)
    # Pivot the table to create the matrix
    matrix = df.pivot(index='id1', columns='id2', values='result').fillna(0)
    # Fill missing symmetric values in the matrix
    matrix = matrix.combine_first(matrix.T).fillna(0)
    # Save the matrix to the specified Pickle file
    with open(pickle_output_file, 'wb') as f:
        pickle.dump(matrix, f)
    return matrix
