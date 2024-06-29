"""
Original image can be in JPEG or PNG (with alpha channel or without it) formats.
How to build a color palette with bins with their height using Python and openCV?
each bin should represent a color and height of bin should represent a number of pixels of that color.
"""

import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = sys.argv[0]

# Load the image
image = cv2.imread(image_path)

# Convert the image from BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Reshape the image to be a list of pixels
pixels = image.reshape(-1, 3).astype(np.float32)  # Ensure pixels are float32

# Perform k-means clustering to find the most dominant colors
k = 5 # number of colors to find
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
_, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Count the number of pixels for each color
_, counts = np.unique(labels, return_counts=True)

# Sort the colors by the number of pixels, in descending order
sorted_colors = centers[np.argsort(-counts)]

# Sort the counts, in descending order
sorted_counts = counts[np.argsort(-counts)]

# Normalize the counts to get the height of the bins
normalized_counts = sorted_counts / sum(sorted_counts)

# Create the bins for the color palette
bins = np.zeros((50, 300, 3), dtype=np.uint8)

# Fill the bins with the respective color
for i in range(k):
    start = int(sum(normalized_counts[:i]) * 300)
    end = int(sum(normalized_counts[:i+1]) * 300)
    bins[:, start:end, :] = sorted_colors[i]

# Display the color palette
plt.imshow(bins)
plt.show()

"""
In this code:

    An image is loaded and converted from BGR to RGB color space.
    The image is reshaped to a list of pixels which is then used in k-means clustering to find the most dominant colors.
    The number of pixels for each color is counted and sorted in descending order.
    The counts are normalized to represent the height of the bins.
    Bins are created and filled with the respective color.

"""
