import React, {Component} from 'react';
import {render} from 'react-dom';
import MapGL, {NavigationControl} from 'react-map-gl';
import ControlPanel from './control-panel';

import BarChart from '../charts/BarChart'
import {defaultMapStyle, dataLayer} from './map-style.js';
import {updatePercentiles} from './utils';
import {fromJS} from 'immutable';
import Axios from 'axios';
import './map.css';

const MAPBOX_TOKEN = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA'; // Set your mapbox token here

export default class App extends Component {
  state = {
    mapStyle: defaultMapStyle,
    year: 2015,
    data: null,
    hoveredFeature: null,
    viewport: {
      latitude: -37.713179,
      longitude: 145.250259,
      zoom: 8,
      bearing: 0,
      pitch: 0
    }
  };

  componentDidMount() {

    Axios.get('http://localhost:50000/melb') // JSON File Path

    .then( response => {
        console.log('get response')
        // this.setState({data:response.data})
        console.log(response.data)
        this._loadData(response.data);
    })

    .catch(function (error) {
      console.log(error);
    });

  }

  _loadData = data => {
    updatePercentiles(data, f => f.properties.grand_total_offence_count);
    
    const mapStyle = defaultMapStyle
      // Add geojson source to map
      .setIn(['sources', 'crimeRateBySuburb'], fromJS({type: 'geojson', data}))
      // Add point layer to map
      .set('layers', defaultMapStyle.get('layers').push(dataLayer));

    this.setState({data, mapStyle});

    console.log(mapStyle)
  };

  _updateSettings = (name, value) => {
    if (name === 'year') {
      this.setState({year: value});

      const {data, mapStyle} = this.state;
      if (data) {
        updatePercentiles(data, f => f.properties.income[value]);
        const newMapStyle = mapStyle.setIn(['sources', 'incomeByState', 'data'], fromJS(data));
        this.setState({mapStyle: newMapStyle});
      }
    }
  };

  _onViewportChange = viewport => this.setState({viewport});

  _onHover = event => {
    const {
      features,
      srcEvent: {offsetX, offsetY}
    } = event;
    const hoveredFeature = features && features.find(f => f.layer.id === 'data');

    this.setState({hoveredFeature, x: offsetX, y: offsetY});
  };

  _renderTooltip() {
    const {hoveredFeature, x, y} = this.state;

    let data = []
    if(hoveredFeature && hoveredFeature.properties.data) {
      var obj = JSON.parse(hoveredFeature.properties)

      for (var k in obj) {
        const tmp = {
          'name': k,
          'value': obj[k]
        }
        data.push(tmp)
      }
    }

    return (
      hoveredFeature && (
        <div className="tooltip" style={{left: x, top: y}}>
          {/* <div>State: {hoveredFeature.properties.lga_name11}</div>
          <div>Total offence count: {hoveredFeature.properties.b40_theft}</div>
          <div>Percentile: {(hoveredFeature.properties.b40_theft / hoveredFeature.properties.grand_total_offence_count) * 100}</div> */}
          <BarChart 
            style={{left: x, top: y}}
            chartData={data}
          >
          </BarChart>
        </div>
        
      )
    );
  }

  render() {
    const {viewport, mapStyle} = this.state;
    
    // console.log(mapStyle)
    
    return (
      <div style={{height: '100%'}}>
        <MapGL
          {...viewport}
          width="100%"
          height={800}
          mapStyle={mapStyle}
          onViewportChange={this._onViewportChange}
          mapboxApiAccessToken={MAPBOX_TOKEN}
          onHover={this._onHover}
        >
          {this._renderTooltip()}

          <div style={{position: 'absolute', left: 10, top: 10}}>
                <NavigationControl onViewportChange={this._onViewportChange} />
          </div>
        </MapGL>

        <ControlPanel
          containerComponent={this.props.containerComponent}
          settings={this.state}
          onChange={this._updateSettings}
        />
      </div>
    );
  }
}

export function renderToDom(container) {
  render(<App />, container);
}
