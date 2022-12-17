import json
import numpy as np
import matplotlib.pyplot as plt

from image.image_service import ImageService

from config import TARGETS_SCANNING_IMAGE
from matplotlib.widgets import Slider, Button


class VisualizerService:
    def __init__(self, mission_targets: str = TARGETS_SCANNING_IMAGE) -> None:
        self.imageservice = ImageService(mission_targets)

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

        targets = self.imageservice.target_shell_list

        x_values = np.array([])
        y_values = np.array([])

        for target_point in targets:
            (key, value), = target_point.items()
            x_values = np.append(x_values, [key for _ in range(len(value))])
            y_values = np.append(y_values, value)

        ax.scatter(x_values, y_values)

        plt.show()
    
    @staticmethod
    def show_output():
        with open('data/output.json') as f:
            output = json.loads(f.read())

        def f(frequency):

            return [i ** 2 + frequency for i in range(10)]

        t = [i for i in range(10)]

        # Define initial parameters
        init_amplitude = 5

        # Create the figure and the line that we will manipulate
        fig, ax = plt.subplots()
        line = ax.scatter(t, f(t))
        ax.set_xlabel('Time [s]')

        # adjust the main plot to make room for the sliders
        fig.subplots_adjust(left=0.25, bottom=0.25)

        # Make a horizontal slider to control the frequency.

        # Make a vertically oriented slider to control the amplitude
        axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
        amp_slider = Slider(
            ax=axamp,
            label="Amplitude",
            valmin=0,
            valmax=10,
            valinit=init_amplitude,
            orientation="vertical"
        )


        # The function to be called anytime a slider's value changes
        def update(val):
            # line.set_ydata(f(t, amp_slider.val, 1))
            line = ax.scatter(t, f(amp_slider.val))
            fig.canvas.draw_idle()


        # register the update function with each slider
        amp_slider.on_changed(update)

        # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
        resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
        button = Button(resetax, 'Reset', hovercolor='0.975')


        def reset(event):
            amp_slider.reset()
        button.on_clicked(reset)

        plt.show()