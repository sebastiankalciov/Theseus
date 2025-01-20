import * as d3 from "d3";
import React, { useEffect, useRef } from 'react';
import {useLocation} from "react-router-dom";

const AnimationPage = () => {
    const { state } = useLocation();
    const data = state?.data;

    const svgRef = useRef();
    useEffect(() => {
        if (data) {

            // extract data from the graph json: the points, shortest path and the outline of the polygon
            const { points, path, outline } = data;

            const width = 1300, height = 1000;
            const svg = d3.select("svg");

            // scale the points
            // because when they are first processed they have large values (> 1000)
            const xScale = d3.scaleLinear()
                .domain(d3.extent(points, d => d[0]))
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain(d3.extent(points, d => d[1]))
                .range([0, height]);

            const scaledPoints = points.map(([x, y]) => [xScale(x), yScale(y)]);

            // draw polygon outline
            svg.append("path")
                .datum([...outline, outline[0]])
                .attr("d", d3.line()
                    .x(d => xScale(d[0]))
                    .y(d => yScale(d[1]))
                )
                .attr("fill", "none")
                .attr("stroke", "black")
                .attr("stroke-width", 3);

            // draw path
            svg.append("path")
                .datum(path.coordinates)
                .attr("d", d3.line()
                    .x(d => xScale(d[0]))
                    .y(d => yScale(d[1]))
                )
                .attr("fill", "none")
                .attr("stroke", "red")
                .attr("stroke-width", 4);
        }
    }, [data]);
    
    return (
        <div className={"AnimationPage"} style = {{justifyContent:"center", alignItems:"center", display:"flex", flexDirection:"column"}}>
            <h1>Polygon with shortest path</h1>
            <svg ref={svgRef} width={1500} height={1000}></svg>
        </div>
    )
};

export default AnimationPage;