import numpy as np
import matplotlib.pyplot as plt

from image_service import ImageService


class VisualizerService:
    def __init__(self) -> None:
        self.imageservice = ImageService()

    def show_area(self):

        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(projection='3d')

        image = self.imageservice.mission_area

        x_values = np.array([])
        y_values = np.array([])
        z_values = np.array([])

        for i, row in enumerate(image):
            for j, color_list in enumerate(row):
                x_values = np.append(x_values, i)
                y_values = np.append(y_values, j)
                z_values = np.append(z_values, self.imageservice.get_color_value(color_list))

        ax.scatter(x_values, y_values, z_values, c=z_values, zdir='z', cmap='Accent')

        plt.show()

    def show_targets(self):
        fig = plt.figure(figsize=(120, 120))
        ax = fig.add_subplot()

        targets = self.imageservice.get_targets_coords()

        x_values = []
        y_values = []

        for target_point in targets:
            x_values.append(target_point.x)
            y_values.append(target_point.y)

        ax.scatter(x_values, y_values)

        plt.show()


VisualizerService().show_targets()
