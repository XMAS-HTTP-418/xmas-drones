import numpy as np
import matplotlib.pyplot as plt

from image_service import ImageService

imageservice = ImageService()

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')

image = imageservice.mission_area

x_values = np.array([])
y_values = np.array([])
z_values = np.array([])

for i, row in enumerate(image):
    for j, color_list in enumerate(row):
        x_values = np.append(x_values, i)
        y_values = np.append(y_values, j)
        z_values = np.append(z_values, imageservice.get_color_value(color_list))


ax.scatter(x_values, y_values, z_values, c=z_values, zdir='z', cmap='Accent')

plt.show()