import numpy as np
import cv2
import os
import pandas as pd
from skimage.metrics import structural_similarity as ssim, peak_signal_noise_ratio as psnr
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)
# load the first image
image1 = cv2.imread('/sources/images\\days_seconds\\alpha_red_scatter\\0.png')

# path to the directory containing the other images
directory = 'C:\\Users\\agrri\\PycharmProjects\\TCC\\project\\images\\days_seconds\\alpha_red_scatter'

df_mse = pd.DataFrame(columns=['Image1', 'Image2', 'MSE'])
df_nrmse = pd.DataFrame(columns=['Image1', 'Image2', 'NRMSE'])
df_ssim = pd.DataFrame(columns=['Image1', 'Image2', 'SSIM'])
df_psnr = pd.DataFrame(columns=['Image1', 'Image2', 'PSNR'])

images = [f for f in os.listdir(directory) if f.endswith('.png')]  # assuming the images are in png format

for i in range(len(images)):
    for j in range(i+1, len(images)):
        print(i,j)
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

        df_mse = pd.concat([df_mse, pd.DataFrame([{'Image1': images[i], 'Image2': images[j], 'MSE': mse}])],
                           ignore_index=True)
        df_nrmse = pd.concat([df_nrmse, pd.DataFrame([{'Image1': images[i], 'Image2': images[j], 'NRMSE': nrmse}])],
                             ignore_index=True)
        df_ssim = pd.concat([df_ssim, pd.DataFrame([{'Image1': images[i], 'Image2': images[j], 'SSIM': ssim_val}])],
                            ignore_index=True)
        df_psnr = pd.concat([df_psnr, pd.DataFrame([{'Image1': images[i], 'Image2': images[j], 'PSNR': psnr_val}])],
                            ignore_index=True)

# save the dataframes to csv
df_mse.to_csv('C:\\Users\\agrri\\PycharmProjects\\TCC\\project\\images\\days_seconds\\mse_comparison.csv', index=False)
df_nrmse.to_csv('C:\\Users\\agrri\\PycharmProjects\\TCC\\project\\images\\days_seconds\\nrmse_comparison.csv', index=False)
df_ssim.to_csv('C:\\Users\\agrri\\PycharmProjects\\TCC\\project\\images\\days_seconds\\ssim_comparison.csv', index=False)
df_psnr.to_csv('C:\\Users\\agrri\\PycharmProjects\\TCC\\project\\images\\days_seconds\\psnr_comparison.csv', index=False)
