
from image.image_service import TargetType
from image import ImageService, VisualizerService
from config import TARGETS_SCANNING_IMAGE

# if __name__ == "__main__":
#     # ImageService()
    
    
#     visualizer = VisualizerService(TARGETS_SCANNING_IMAGE)  # put your filename here
#     # visualizer.show_area()
#     visualizer.show_targets()




def get_targets_coords(image) -> list:
    """
    Получаем координаты цели
    """
    target_coords = []
    target_shell_list = {}
    for i, row in enumerate(image):
        target_shell = []
        j = 0
        while j < len(row) - 1:
            sublist = []
            while (row[j] != 5) and (row[j] != 4):
                sublist.append(j)

                if j < len(row) - 1:
                    j += 1
                else:
                    sublist.append(j)
                    break

            if sublist:
                target_shell.append(sublist)
            j += 1

        for sublist in target_shell:
            target_shell_list[i] = target_shell_list.get(i, [])
            target_shell_list[i].append(sublist)
            
        
        target_shell_s = []
        k = 0
        while k < len(target_shell_list) - 1:
            sublist = []
            while target_shell_list.get(k) and (target_shell_list[k] != 5) and (target_shell_list[k] != 4):
                sublist.append(k)

                if k < len(row) - 1:
                    k += 1
                else:
                    sublist.append(k)
                    break

            if sublist:
                target_shell_s.append(sublist)
            k += 1


    return target_shell_s


test_image = [
    [1, 1, 5, 1, 1, 1],
    [1, 5, 1, 1, 1, 1],
    [5, 5, 1, 5, 5, 5],
    [1, 1, 5, 5, 5, 5]
]
get_targets_coords(test_image)

from image import ImageService, VisualizerService
from config import TARGETS_SCANNING_IMAGE

if __name__ == "__main__":
    # ImageService()

    visualizer = VisualizerService(TARGETS_SCANNING_IMAGE)  # put your filename here
    # visualizer.show_area()
    visualizer.show_targets()
