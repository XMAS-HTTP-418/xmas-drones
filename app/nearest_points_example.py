from image.image_service import ImageService
from search import nearest_neighbor_kdtree


imageservice = ImageService()
nearest_points = nearest_neighbor_kdtree(query_points=[(20, 2)], reference_points=imageservice.targets_coords)
print(nearest_points)
