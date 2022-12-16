from data_parser import DataParser
from mission_assignment import calculate_task_assignments, get_cost_matrix, assign_tasks

DataParser.load_data('data/input.json')
cost_matrix = get_cost_matrix(DataParser.drones,DataParser.missions)
tasks = calculate_task_assignments(cost_matrix)
assign_tasks(DataParser.drones, DataParser.missions, tasks)
