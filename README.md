# Theseus

**Theseus** is a mobile & web application developed to compute the shortest path in a polygon and visual represent it on the web.

## Polygon with shortest path on web

<img src = "./assets/polygon_with_shortest_path.png" width = 700/>

## Raw image of polygon

<img src = "./assets/raw_polygon_image.jpg" width = 700/>


## Polygon outline

<img src = "./assets/processed_overlay1.png" width = 700/>

## Matplotlib polygon with triangulation andshortest path representation

<img src = "./assets/matplotlib.png" width = 700/>


## Mobile view

<img src = "./assets/mobile_view.png" width = 350 height = 800/>

## Web view

<img src = "./assets/web_view.png" width = 700/>

## Flow

- Draw on a paper a simple polygon
- Place the phone above a paper
- Take picture and send image to firebase
- Process image from firebase (opencv) then compute the graph
- Use Dijsktra to compute the shortest path
- Represent visually the shortest path on the web using D3.js

Note: This is a simple representation of the app's flow

## Technical details

- Mobile: **React Native**
- Database: **Firebase**
- Web client: **React**
- Web server: **Express**


- Image processing: Python, **OpenCV**
- Graph computation: Python (**scipy, shapely, matplotlib**)
- Triangulation: **Delaunay's** algorithm for triangulation
- Path computation: **Dijkstra's** shortest path algorithm
- Graph representation: **D3.js**

### Reference

The project's name is a Greek mythology reference to the labyrinth in which [Theseus](https://en.wikipedia.org/wiki/Theseus) fought the Minotaur.
