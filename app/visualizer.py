from array import array
import matplotlib.pyplot as plt

from height_map import get_mission_area, get_color_value

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')

image = get_mission_area()

x_values = array('i')
y_values = array('i')
z_values = array('i')

for i, row in enumerate(image):
    for j, color_list in enumerate(row):
        x_values.append(i)
        y_values.append(j)
        z_values.append(get_color_value(color_list))


ax.scatter(x_values, y_values, z_values, c=z_values, zdir='z', cmap='Accent')

plt.show()