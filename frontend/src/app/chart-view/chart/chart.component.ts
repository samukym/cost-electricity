import { Component, Input } from '@angular/core';
import * as d3 from 'd3';
import { CostSlot } from '../chart-view.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent {

  @Input() consumeCost: Array<CostSlot> = [];

  private svg: any;

  constructor() { }

  ngOnChanges() {
    this.drawGraph(this.consumeCost)
  }

  private drawGraph(data: Array<CostSlot>) {
    const margin = { top: 20, right: 30, bottom: 30, left: 60 },
      width = 800 - margin.left - margin.right,
      height = 600 - margin.top - margin.bottom;

    d3.select('svg').remove();

    this.svg = d3.select('#chart')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    data.forEach(d => {
      d.timestamp = d.timestamp;
      d.cost = d.cost;
    });

    const x = d3.scaleTime()
      .domain(<[Date, Date]>d3.extent(data, d => d.timestamp))
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, <number>d3.max(data, d => d.cost)])
      .range([height, 0]);

    const line = d3.line<{ timestamp: Date, cost: number }>()
      .x(d => x(d.timestamp))
      .y(d => y(d.cost));

    this.svg.append('path')
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr('class', 'line')
      .attr('d', line);

    this.svg.append('g')
      .attr('transform', 'translate(0,' + height + ')')
      .call(d3.axisBottom(x));

    this.svg.append('g')
      .call(d3.axisLeft(y));
  }
}

