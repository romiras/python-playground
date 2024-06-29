"""
How to build a color palette with bins with their height using Python and openCV?
"""

import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

def build_color_palette(image, bin_count):
    # Flatten the image
    pixels = image.reshape(-1, 3)
    # Perform k-means clustering to find the most dominant colors
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels.astype(float), bin_count, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Count the frequency of each label
    _, counts = np.unique(labels, return_counts=True)
    # Sort the centers by the frequency of each label
    dominant_colors = centers[np.argsort(-counts)]
    # Normalize the counts for plotting
    counts = counts / float(sum(counts))
    # Create the color palette
    palette = np.zeros((50, 300, 3), dtype=np.uint8)
    start = 0
    for i in range(bin_count):
        end = start + counts[i]*300
        r, g, b = dominant_colors[i]
        cv2.rectangle(palette, (int(start), 0), (int(end), 50), (r,g,b), -1)
        start = end	
    # Display the color palette
    plt.figure()
    plt.axis("off")
    plt.imshow(palette)
    plt.show()

image_path = sys.argv[0]

# Load the image
# image = cv2.imread(image_path)
image = cv2.imread(image_path, cv2.IMREAD_COLOR)

# Convert the image from BGR to RGB
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# converting it to a 3-channel image (required for PNG files)
image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)

# plt.figure()
# plt.axis("off")
# plt.imshow(image)
# plt.show()

# sys.exit(1)

# Call the function with the path to your image and the number of bins
build_color_palette(image, 5)
