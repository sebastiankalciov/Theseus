import numpy as np
import urllib.request
import cv2
import sys
from scipy.spatial import Delaunay
from shapely.geometry import LineString, Polygon
import matplotlib.pyplot as plt
import heapq
import json

def url_to_image(url):
    # open a connection with url
    response = urllib.request.urlopen(url)

    # convert the raw image into numpy array
    image = np.asarray(bytearray(response.read()), dtype="uint8")

    # transform the image into something opencv can work with
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

    return image

# compute the euclidean distance between 2 points on the image
def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# calculate the center of the start/end point
def calculate_centroid(contour):
    M = cv2.moments(contour)

    if M["m00"] == 0:
        return None
    
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    return (cx, cy)

# implementation of dijkstra algorithm for shortest path
def compute_path(graph, start, end):
    queue = [(0, start)]
    distances = {i: float('inf') for i in graph}
    distances[start] = 0
    previous = {i: None for i in graph}
    
    while queue:
        current_distance, current_vertex = heapq.heappop(queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(queue, (distance, neighbor))
        
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    return path[::-1]

# build a graph from Delaunay triangulation
def build_graph_from_triangulation(points, triangles, polygon_points, with_points=True):
    
    polygon = Polygon(polygon_points)
    graph = {i: [] for i in range(len(points))}
    centroids = []
    centroid_indices = {}

    # calculate centroids (start & end points) for triangles and add them as new points
    for t, triangle in enumerate(triangles):
        triangle_points = [points[triangle[0]], points[triangle[1]], points[triangle[2]]]
        centroid = np.mean(triangle_points, axis=0)
        centroids.append(centroid)
        centroid_indices[t] = len(points) + len(centroids) - 1
        graph[centroid_indices[t]] = []

    # add edges between centroids (start & end points) and triangle vertices if valid
    for t, triangle in enumerate(triangles):
        i, j, k = triangle
        triangle_edges = [
            (i, j, euclidean_distance(points[i], points[j])),
            (j, k, euclidean_distance(points[j], points[k])),
            (k, i, euclidean_distance(points[k], points[i]))
        ]

        for u, v, distance in triangle_edges:
            edge_line = LineString([points[u], points[v]])

            if polygon.contains(edge_line):
                graph[u].append((v, distance))
                graph[v].append((u, distance))

        # add edges between the centroid and triangle vertices
        for vertex in triangle:
            edge_line = LineString([points[vertex], centroids[t]])

            # check if the line is inside of the polygon and not outside
            # this messed up a lot of things when it was not checked (couldn't compute the shortest path)
            if polygon.contains(edge_line): 
                graph[centroid_indices[t]].append((vertex, euclidean_distance(points[vertex], centroids[t])))
                graph[vertex].append((centroid_indices[t], euclidean_distance(points[vertex], centroids[t])))

    # add edges between adjacent triangle centroids
    for t1, triangle1 in enumerate(triangles):
        for t2, triangle2 in enumerate(triangles):

            if t1 >= t2:
                continue

            shared_vertices = set(triangle1).intersection(triangle2)

            if len(shared_vertices) == 2:
                centroid1 = centroids[t1]
                centroid2 = centroids[t2]
                edge_line = LineString([centroid1, centroid2])

                if polygon.contains(edge_line):
                    centroid_distance = euclidean_distance(centroid1, centroid2)
                    graph[centroid_indices[t1]].append((centroid_indices[t2], centroid_distance))
                    graph[centroid_indices[t2]].append((centroid_indices[t1], centroid_distance))

    # add centroids to points array
    points = np.vstack([points, centroids])

    if with_points:
        return graph, points
    else:
        return graph

# display triangulation with path
def visualize_triangulation_with_path(points, triangles, path, centroids, polygon_points, graph):
    plt.figure(figsize=(30, 60))
    
    num_polygon_points = len(polygon_points)
    for i in range(num_polygon_points):

        # connect each point to the next, looping back to the start
        point_a = polygon_points[i]
        
        # wrap around to form a closed polygon
        point_b = polygon_points[(i + 1) % num_polygon_points] 

        plt.plot(
            [point_a[0], point_b[0]],
            [point_a[1], point_b[1]],
            'r-', 
            linewidth=10
        )
    
    # draw triangulation
    for triangle in triangles:
        for i, j in [(0, 1), (1, 2), (2, 0)]:
            point_a = points[triangle[i]]
            point_b = points[triangle[j]]
            plt.plot([point_a[0], point_b[0]], [point_a[1], point_b[1]], 'k-', linewidth=1)
        
        i, j, k = triangle
        plt.plot([points[i][0], points[k][0]], [points[i][1], points[k][1]], 'b--', linewidth=2)  # Diagonal (i, k)
        plt.plot([points[j][0], points[k][0]], [points[j][1], points[k][1]], 'b--', linewidth=2) 
    
    # draw points
    for point in points:
        plt.plot(point[0], point[1], 'bo')
    
    # highlight centroids
    for centroid in centroids:
        plt.plot(centroid[0], centroid[1], 'ro', markersize = 30)
        
    # draw shortest path
    for i in range(len(path) - 1):

        start_point = points[path[i]]
        end_point = points[path[i + 1]]
        plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], 'g-', linewidth=15)
        
    plt.gca().invert_yaxis()
    plt.savefig("data-output/testplot1.png", bbox_inches="tight")
    plt.close() 

def save_data(points,path, polygon_outline, output_file="data-output/newprocessed_data.json"):
    points_list = points.tolist()

    path_points = [points[index].tolist() for index in path]

    outline_points = polygon_outline.tolist()

    data = {
        "points": points_list,
        "path": {
            "indices": list(map(int, path)), 
            "coordinates": path_points
        },
        "outline": outline_points
    }

    # data saved in a file is used just for debugging, it has no other role
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return data

def process_image(imageURL):

    image = url_to_image(imageURL);

    _,threshold = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY) 

    # extract the contours
    # RETR_TREE - retrieval mode to get the contours and arrange them in a tree hierarchy
    # CHAIN_APPROX_SIMPLE - contour approximation mode for compression - efficiency
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    polygons = []

    # when the image is first processed
    # it outputs the contour of the paper, 2 contours of the polygon
    # start point, endpoint and noise
    
    areasWithContours = []
    
    # get the polygons with their respective area 
    for contour in contours:
        areasWithContours.append([cv2.contourArea(contour), contour])

    # sort the polygons based on their area size

    sortedAreas = sorted(areasWithContours, reverse=True, key=lambda x: x[0])[1:5]

    # check if the first 2 polygons are not the same
    # because it is possible to extract 2 variants of the polygon
    # (this function is useless rn, but will remain here for future improvements)
    
    if sortedAreas[0][0] > 1000000 and sortedAreas[1][0] > 1000000:
        sortedAreas = sortedAreas[1:5]

    for area, contour in sortedAreas: 

        # take only the large polygons (the main polygon and the starting/ending point) and reduce noise
        # second measure in case something breaks when doing the first sorting

        if area > 4000:  

            # approxPolyDP - approximates the polygon to a specific precision
            # arcLength - computer the perimiter of the shape (polygon)
            approx = cv2.approxPolyDP(contour, 0.005 * cv2.arcLength(contour, True), True) 
            
            # makes sure the polygon has at least 5 edges (have to reconsider this condition)
            if(len(approx) > 5):  

                polygons.append(approx)
                cv2.drawContours(image, [approx], 0, (255, 0, 0), 5) 

    # create a white outline of the polygon on a black background
    canvas = np.zeros_like(image)

    polygon_points_polygon = polygons[0].reshape((-1, 2))

    polygon_points_circle1 = polygons[1].reshape((-1, 1, 2)).astype(np.int32)
    polygon_points_circle2 = polygons[2].reshape((-1, 1, 2)).astype(np.int32)

    circle1 = polygons[1]
    circle2 = polygons[2]

    centroid1 = calculate_centroid(circle1)
    centroid2 = calculate_centroid(circle2)

    if centroid1 is None or centroid2 is None:
        #print("Error: Could not calculate centroids of the circles.")
        return
    
    # combine polygon vertices and circle centroids
    points = np.vstack([polygon_points_polygon, centroid1, centroid2])
    points1 = np.vstack([polygon_points_polygon, centroid1, centroid2])
    triangles = Delaunay(points).simplices

    # build a graph from the triangulation
    graph, points = build_graph_from_triangulation(points, triangles, polygon_points_polygon)
    triangles = Delaunay(points).simplices

    graph, points = build_graph_from_triangulation(points, triangles, polygon_points_polygon)
    
    path = compute_path(graph, len(points1) - 2, len(points1) - 1)

    visualize_triangulation_with_path(points, triangles, path, [centroid1, centroid2], polygon_points_polygon, graph)

    data = save_data(points, path, polygon_points_polygon)

    # create the outline of the drawn polygon
    cv2.polylines(canvas, [polygon_points_polygon], isClosed=True, color=(255, 255, 255), thickness=2)
    cv2.polylines(canvas, [polygon_points_circle1], isClosed=True, color=(255, 255, 255), thickness=2)
    cv2.polylines(canvas, [polygon_points_circle2], isClosed=True, color=(255, 255, 255), thickness=2)
    cv2.imwrite('data-output/processed_overlay1.png', canvas)
    
    # to return the response it must be printed
    print(json.dumps(data))
    return 1

if __name__== "__main__":

    # argv[1] - imageURL
    process_image(sys.argv[1]);