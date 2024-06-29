import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = sys.argv[1]

# Load the image
image = cv2.imread(image_path)

# Convert the image from BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Reshape the image to be a list of pixels
pixels = image.reshape(-1, 3).astype(np.float32)  # Ensure pixels are float32

# Extract hue (H) and value (V) components
hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
hue_values = hsv_image[:, :, 0] / 360.0  # Normalize hue to [0, 1]
value_values = hsv_image[:, :, 2] / 255.0  # Normalize value to [0, 1]

# Create the scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(hue_values, value_values, s=1, c=pixels / 255.0, marker="o")
plt.xlabel("Hue (normalized)")
plt.ylabel("Value (normalized)")
plt.title("Scatter Plot of Colors in HSV Space")
plt.grid(True)
plt.gca().set_facecolor('black')  # Set the background color

plt.show()
