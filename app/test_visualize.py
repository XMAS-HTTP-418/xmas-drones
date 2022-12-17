from image import ImageService, VisualizerService
from config import TARGETS_SCANNING_IMAGE

if __name__ == "__main__":
    # ImageService()

    visualizer = VisualizerService(TARGETS_SCANNING_IMAGE)  # put your filename here
    # visualizer.show_area()
    visualizer.show_targets()
