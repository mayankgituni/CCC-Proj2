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
      const {chartData} = this.props
      
        // console.log(chartData)
        return (
             <BarChart 
                width={550}
                height={400}
                data={chartData}
                margin={{
                    top: 50, right: 30, left: 40, bottom: 20,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name">
                    <Label value="Pages of my website" offset={-10} position="insideBottom" />
                </XAxis>
                <YAxis label={{ value: 'number of events', angle: -90, position: 'insideLeft' }} />
                <Bar dataKey="value" fill="#8884d8">
                    <LabelList dataKey="amt" position="top" />
                </Bar>
            </BarChart>

            // <Widget title="Simple Line Chart" noBodyPadding upperTitle>
            // <ResponsiveContainer width="100%" height={350}>
            //     <lineChart
            //         width={500}
            //         height={300}
            //         data={lineChartData}
            //         margin={{
            //             top: 5, right: 30, left: 20, bottom: 5,
            //         }}
            //     >
            //         <CartesianGrid strokeDasharray="3 3" />
            //         <XAxis dataKey="name" />
            //         <YAxis />
            //         <Tooltip />
            //         <Legend />
            //         {/* <Line type="monotone" dataKey="pv" stroke={props.theme.palette.primary.main} activeDot={{ r: 8 }} />
            //         <Line type="monotone" dataKey="uv" stroke={props.theme.palette.secondary.main} /> */}
            //     </LineChart>
            // </ResponsiveContainer>
            // </Widget>

        )
    }
}

