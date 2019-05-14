import React, { Component } from 'react'
import MapGL, { Popup, NavigationControl} from 'react-map-gl';
import {fromJS} from 'immutable';
import {json as requestJson} from 'd3-request';
import {defaultMapStyle, dataLayer} from './map-style.js';
import Axios from 'axios'

// Set your mapbox token here
const TOKEN = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA'; 


const navStyle = {
  position: 'absolute',
  top: 0,
  left: 0,
  padding: '10px'
};



export default class Map extends Component {
  constructor(props) {
      super(props);
      this.state = {
        mapStyle: defaultMapStyle,
        year: 2015,
        data: null,
        hoveredFeature: null,
        viewport: {
          latitude: 40,
          longitude: -100,
          zoom: 3,
          bearing: 0,
          pitch: 0,
          width: `100%`,
          height: 800,
        }
      };
    }

    componentDidMount() {

      Axios.get('http://localhost:5000/usa') // JSON File Path

          .then( response => {
              console.log('get response')
              this._loadData(response.data)
          })
          .catch(function (error) {
            console.log(error);
          });


      }
  
    _loadData = data => {

        console.log(data)
        const mapStyle = fromJS({
          version: 8,
          sources: {
              points: {
                  type: 'geojson',
                  data: data
              }
          },
          layers: defaultMapStyle.get('layers').push(dataLayer)
      });

        // const mapStyle = defaultMapStyle
        // // Add geojson source to map
        // .setIn(['sources', 'points'], fromJS({type: 'geojson', data}))
        // // Add point layer to map
        // .set('layers', defaultMapStyle.get('layers').push(dataLayer));

        // this.setState({data, mapStyle});
    };
  
    // _updateSettings = (name, value) => {
    //   if (name === 'year') {
    //     this.setState({year: value});
  
    //     const {data, mapStyle} = this.state;
    //     if (data) {
    //       updatePercentiles(data, f => f.properties.income[value]);
    //       const newMapStyle = mapStyle.setIn(['sources', 'incomeByState', 'data'], fromJS(data));
    //       this.setState({mapStyle: newMapStyle});
    //     }
    //   }
    // };
  
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
  
      return (
        hoveredFeature && (
          <div className="tooltip" style={{left: x, top: y}}>
            <div>State: {hoveredFeature.properties.name}</div>
            <div>Median Household Income: {hoveredFeature.properties.value}</div>
            <div>Percentile: {(hoveredFeature.properties.percentile / 8) * 100}</div>
          </div>
        )
      );
    }

  render() {
      const {viewport, mapStyle} = this.state;
      return (
            <MapGL
              {...viewport}
              // mapStyle={mapStyle}
              onViewportChange={this._onViewportChange}
              mapStyle="mapbox://styles/mapbox/dark-v9"
              mapboxApiAccessToken={TOKEN}
              // onHover={this._onHover}  
            >
              <div className="nav" style={navStyle}>
                <NavigationControl/>
              </div>
            </MapGL>
      );
    }
}