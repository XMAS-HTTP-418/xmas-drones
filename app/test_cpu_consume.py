# import psutil
# # gives a single float value
# psutil.cpu_percent()
# # gives an object with many fields
# psutil.virtual_memory()
# # you can convert that object to a dictionary
# dict(psutil.virtual_memory()._asdict())
# # you can have the percentage of used RAM
# psutil.virtual_memory().percent
# # you can calculate percentage of available memory
# a = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
# print(psutil.cpu_percent())
# print(psutil.virtual_memory())

import numpy as np
from PIL import Image

from config import TARGETS_SCANNING_IMAGE

im = Image.open(TARGETS_SCANNING_IMAGE).convert("L")  # Can be many different formats.
data = iter(im.getdata())
rows, cows = im.size

a = np.array(tuple(np.array(tuple(next(data) for j in range(cows)), dtype="uint8") for i in range(rows)))
a.shape
