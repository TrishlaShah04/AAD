from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

# Function to calculate shortest path using Dijkstra's algorithm
def compute_shortest_path(network, starting_point):
    path_distances = {point: float('infinity') for point in network}
    path_distances[starting_point] = 0
    priority_queue = [(0, starting_point)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > path_distances[current_node]:
            continue
        
        for adjacent, cost in network[current_node]:
            new_distance = current_distance + cost
            
            if new_distance < path_distances[adjacent]:
                path_distances[adjacent] = new_distance
                heapq.heappush(priority_queue, (new_distance, adjacent))
                
    return path_distances

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get number of points and create the network
        total_points = int(request.form['num_nodes'])
        points = [request.form.get(f'node_{i}') for i in range(total_points)]
        
        # Initialize network as an empty dictionary
        network = {point: [] for point in points}
        
        # Get edges from user input
        total_edges = int(request.form['num_edges'])
        
        for i in range(total_edges):
            start_point = request.form.get(f'edge_{i}_source')
            end_point = request.form.get(f'edge_{i}_destination')
            edge_cost = request.form.get(f'edge_{i}_weight')
            
            # Validate and convert edge_cost to integer
            try:
                edge_cost = int(edge_cost)
            except (TypeError, ValueError):
                return "Error: All edge costs must be valid integers.", 400
            
            # Ensure start and end points are valid
            if start_point not in network or end_point not in network:
                return "Error: Start or end point does not exist in the list of points.", 400
            
            network[start_point].append((end_point, edge_cost))
            network[end_point].append((start_point, edge_cost))  # Assuming undirected graph
        
        # Get the starting point for shortest path calculation
        starting_point = request.form.get('source_node')
        
        if starting_point not in network:
            return "Error: Starting point does not exist in the list of points.", 400
        
        shortest_paths = compute_shortest_path(network, starting_point)
        
        return render_template('index.html', network=network, shortest_paths=shortest_paths, source_node=starting_point, points=points)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
