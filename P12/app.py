from flask import Flask, render_template, request
from itertools import permutations
import numpy as np

app = Flask(__name__)

# Solve the Traveling Salesman Problem
def solve_tsp(distance_matrix):
    num_cities = len(distance_matrix)
    min_cost = float('inf')
    best_path = []
    best_segments = []

    # Iterate over all permutations of the cities
    for city_order in permutations(range(num_cities)):
        current_cost = 0
        segments = []

        # Calculate the cost of the current path
        for i in range(num_cities):
            current_cost += distance_matrix[city_order[i]][city_order[(i + 1) % num_cities]]
            segments.append(
                (city_order[i] + 1, city_order[(i + 1) % num_cities] + 1,
                 distance_matrix[city_order[i]][city_order[(i + 1) % num_cities]])
            )

        # Update the minimum cost and best path if the current cost is lower
        if current_cost < min_cost:
            min_cost = current_cost
            best_path = city_order
            best_segments = segments

    return best_path, min_cost, best_segments

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the number of cities
        city_count = int(request.form['city_count'])
        distance_matrix = np.full((city_count, city_count), np.inf)
        input_matrix = []

        # Build the distance matrix from form inputs
        for i in range(city_count):
            row = []
            for j in range(city_count):
                distance_key = f'distance_{i}_{j}'
                distance_value = request.form[distance_key]

                if distance_value == '∞' or distance_value == '':
                    distance_matrix[i][j] = float('inf')  # Treat '∞' as infinity
                else:
                    distance_matrix[i][j] = int(distance_value)
                row.append(distance_value)
            input_matrix.append(row)

        # Solve the Traveling Salesman Problem
        best_path, min_cost, path_segments = solve_tsp(distance_matrix)

        # Format the results
        formatted_path = ' - '.join(str(city + 1) for city in best_path) + ' - 1'
        formatted_segments = ', '.join(
            [f"{start} - {end} = {cost}" for start, end, cost in path_segments]
        )

        result = {
            'path': formatted_path,
            'cost': min_cost,
            'input_matrix': input_matrix,
            'segments': formatted_segments,
        }

        return render_template('index.html', result=result)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
