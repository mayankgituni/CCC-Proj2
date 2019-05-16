import React from 'react';
import Widget from '../../components/Widget';
import {
    CartesianGrid,
    Legend,
    Line,
    LineChart,
    BarChart,
    ResponsiveContainer, Sector,
    Tooltip,
    Bar,
    Label,
    LabelList,
    XAxis,
    YAxis
  } from "recharts";
  


export default class SimpleBarChart extends React.Component {


  constructor(props) {
    super(props);
    this.state = {
      // data: barchartdata
    };
  }

    render() {
      const {chartData,  totalOffence} = this.props
      
        // console.log(chartData)
        return (
             <BarChart 
                width={550}
                height={400}
                data={chartData}
                margin={{
                    top: 50, right: 30, left: 0, bottom: 20,
                }}
            >
                <CartesianGrid strokeDasharray="2 2" />
                <XAxis dataKey="name">
                    <Label value={`Total Offence: ${totalOffence}`} offset={-20} position="insideBottom" />
                </XAxis>
                <Tooltip />
                <YAxis label={{ value: 'number of events',  angle: -90, position: 'insideLeft' }} />
                <Bar dataKey="value" fill="#8884d8">
                    <LabelList dataKey="amt" position="top" />
                </Bar>
            </BarChart>


        )
    }
}

