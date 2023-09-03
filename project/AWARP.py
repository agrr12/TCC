import numpy as np
import pandas as pd
def ConstrainedAWARP(x, y, w):
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

df = pd.read_csv('CSVs/encoded_minutes.csv')[:50:]

# Create an empty dataframe with columns 'id1', 'id2', and 'result'
results_df = pd.DataFrame(columns=['id1', 'id2', 'result'])

for x1, y1 in df.iterrows():
    #print("min", x1)
    id1 = y1['authorChannelId']
    series1 = [int(i) for i in y1['encode_min'].strip('[]').split(',')]
    for x2, y2 in df[int(x1) + 1:].iterrows():
        print("min", x1,x2)
        id2 = y2['authorChannelId']
        series2 = [int(i) for i in y2['encode_min'].strip('[]').split(',')]
        result = ConstrainedAWARP(series1, series2, 100)[0]
        # Append the results to the new dataframe
        results_df.loc[len(results_df)] = [id1, id2, result]

results_df.to_csv('CAWARP_results_minutes_100.csv', index=False)

df = pd.read_csv('CSVs/encoded_seconds.csv')[:50:]
results_df = pd.DataFrame(columns=['id1', 'id2', 'result'])
for x1, y1 in df.iterrows():
    print("sec", x1)
    id1 = y1['authorChannelId']
    series1 = [int(i) for i in y1['encode_sec'].strip('[]').split(',')]
    for x2, y2 in df[int(x1) + 1:].iterrows():
        id2 = y2['authorChannelId']
        series2 = [int(i) for i in y2['encode_sec'].strip('[]').split(',')]
        result = ConstrainedAWARP(series1, series2, 100)[0]
        # Append the results to the new dataframe
        results_df.loc[len(results_df)] = [id1, id2, result]

results_df.to_csv('CAWARP_results_seconds_100.csv', index=False)

df = pd.read_csv('CSVs/encoded_hours.csv')[:50:]
results_df = pd.DataFrame(columns=['id1', 'id2', 'result'])
for x1, y1 in df.iterrows():
    print("hou", x1)
    id1 = y1['authorChannelId']
    series1 = [int(i) for i in y1['encode_hou'].strip('[]').split(',')]
    for x2, y2 in df[int(x1) + 1:].iterrows():
        id2 = y2['authorChannelId']
        series2 = [int(i) for i in y2['encode_hou'].strip('[]').split(',')]
        result = ConstrainedAWARP(series1, series2, 100)[0]
        # Append the results to the new dataframe
        results_df.loc[len(results_df)] = [id1, id2, result]

results_df.to_csv('CAWARP_results_hours_100.csv', index=False)