import csv
import heapq

def load_graph(filename):
    """
    Reads the CSV file and builds an undirected graph.
    Each key in the graph is a station name, with a list of tuples (neighbor, cost, time).
    """
    graph = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header if present
        for row in reader:
            # Expecting row: Departure, Destination, Cost, Time
            if len(row) < 4:
                continue  # skip malformed rows
            station1, station2, cost, time = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()
            try:
                cost = float(cost)
                time = float(time)
            except ValueError:
                continue  # skip rows with invalid numbers

            if station1 not in graph:
                graph[station1] = []
            if station2 not in graph:
                graph[station2] = []
            # Add edge in both directions since the connection works either way
            graph[station1].append((station2, cost, time))
            graph[station2].append((station1, cost, time))
    return graph

def dijkstra(graph, start, end, mode='cheapest'):
    """
    Performs Dijkstra's algorithm on the graph starting from 'start'.
    The 'mode' parameter determines which weight to use:
      - 'cheapest': use cost
      - 'fastest': use time
    Returns:
      - distances: dictionary of minimum accumulated weights from start to each station.
      - previous: dictionary for backtracking the optimal path.
    """
    # Initialize distances and previous dictionaries
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    # Priority queue stores tuples: (accumulated_weight, station)
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        if current_node == end:
            break

        for neighbor, cost, time in graph[current_node]:
            weight = cost if mode == 'cheapest' else time
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    return distances, previous

def reconstruct_path(previous, start, end):
    """
    Reconstructs the path from start to end using the 'previous' dictionary.
    """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path

def calculate_totals(graph, path):
    """
    Calculates the total cost and total time for a given path.
    """
    total_cost = 0
    total_time = 0
    for i in range(len(path) - 1):
        station = path[i]
        next_station = path[i+1]
        # Find the edge that connects the two stations
        for neighbor, cost, time in graph[station]:
            if neighbor == next_station:
                total_cost += cost
                total_time += time
                break
    return total_cost, total_time

def main():
    filename = "task1_3/task1_3_data.csv"
    try:
        graph = load_graph(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    departure = input("Enter departure station: ").strip()
    destination = input("Enter destination station: ").strip()

    if departure not in graph:
        print("Departure station not found in the network.")
        return
    if destination not in graph:
        print("Destination station not found in the network.")
        return

    mode = input("Enter mode ('cheapest' for lowest cost, 'fastest' for shortest time): ").strip().lower()
    if mode not in ('cheapest', 'fastest'):
        print("Invalid mode selected. Defaulting to 'cheapest'.")
        mode = 'cheapest'

    distances, previous = dijkstra(graph, departure, destination, mode)
    if distances[destination] == float('inf'):
        print("No route found between the specified stations.")
        return

    path = reconstruct_path(previous, departure, destination)
    total_cost, total_time = calculate_totals(graph, path)

    print("\nRoute found:")
    print(" -> ".join(path))
    print(f"Total cost: {total_cost}")
    print(f"Total time: {total_time} minutes")

if __name__ == "__main__":
    main()
