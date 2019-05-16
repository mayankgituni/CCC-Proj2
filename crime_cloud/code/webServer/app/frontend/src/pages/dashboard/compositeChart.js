import React, { PureComponent } from 'react';
import {
    ResponsiveContainer, ComposedChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  } from 'recharts';
import Axios from 'axios';

const CustomTooltip = ({ active, payload, label }) => {
    if (active) {
        return (
        <div className="custom-tooltip">
            <p className="label">{`${label} : ${payload[0].value}`}</p>
            <p className="desc">District: </p>
        </div>
        );
    }
    
    return null;
    };


export default class Example extends PureComponent {

    state = {
        isFetching: false,
        data:null,
        properties:null
    };


    componentWillMount() {
        this.setState({isFetching:true})

        Axios.get(`http://localhost:50000/tweet/melb`) // JSON File Path
    
        .then( response => {
            this.setState({data:response.data.features})
            let feature_list = response.data.features
            console.log(response.data)
            let tmp = []
            feature_list.map((district) => tmp.push(district.properties))
            tmp.forEach(function(item) {
                // console.log(item.data)
                // let suicide = item.data.dth_suic_slf_inj_0_74_yrs_2011_15_num ? item.data.dth_suic_slf_inj_0_74_yrs_2011_15_num:0
                // let suicide = item.data.dth_suic_slf_inj_0_74_yrs_2011_15_num ? item.data.dth_suic_slf_inj_0_74_yrs_2011_15_num:0
            });
            this.setState({properties:tmp})
            this.setState({isFetching:false})
        })
    
        .catch(function (error) {
          console.log(error);
        });

    }

    // componentDidMount() {

    //     // Axios.get(`http://localhost:50000/melb/aurinmelb`) // JSON File Path
    //     // Axios.get(`http://`) // JSON File Path
       

    //   }

  render() {

    return (
    <div style={{ width: '100%', height: 500 }}>
        <ResponsiveContainer>
            <ComposedChart
                width={1300}
                height={500}
                data={this.state.properties}
                margin={{
                top: 10, right: 20, bottom: 60, left: 20,
                }}
            >   
                <Legend verticalAlign="top"/>
                <CartesianGrid stroke="#f5f5f5" />
                <XAxis 
                dataKey="lga_name" 
                angle={-90}
                // tick={{fontSize: 14 }}
                textAnchor="end" 
                tickLine={false}
                />
                <YAxis />
                {/* <Tooltip /> */}
                <Tooltip />
                {/* <Area type="monotone" dataKey="amt" fill="#8884d8" stroke="#8884d8" /> */}
                <Bar dataKey="IE" barSize={10} fill="#413ea0" />
                <Line type="monotone" dataKey="data.ppl_who_feel_safe_on_streets_alone_perc" stroke="#333399" />
                <Line type="monotone" dataKey="E" stroke="#008080" />
                <Line type="monotone" dataKey="data.suic_slf_inj_p_0_74_yrs_2011_15_num" stroke="#ff6357" />
                {/* <Scatter dataKey="cnt" fill="red" /> */}
            </ComposedChart>
        </ResponsiveContainer>
      </div>

    );
  }
}