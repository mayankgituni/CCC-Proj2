import React, { Component } from 'react';
import MapGL, { Source, Layer } from '@urbica/react-map-gl';
import Axios from 'axios'
import 'mapbox-gl/dist/mapbox-gl.css';

const TOKEN = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA'; 


export default class Map extends Component {
  constructor(props) {
      super(props);
      this.state = {
        data: null,
        viewport: {
          latitude: -37.813179,
          longitude: 144.950259, 
          zoom: 8,
          bearing: 0,
          pitch: 0,
          width: `100%`,
          height: 800,
        }
      };
    }



    componentDidMount() {

      Axios.get('http://localhost:50000/melb') // JSON File Path

      .then( response => {
          console.log('get response')
          this.setState({data:response.data})
          console.log(response.data)
      })

      .catch(function (error) {
        console.log(error);
      });

    }
  

 

  render() {
      const {viewport, mapStyle} = this.state;
      return (
            <MapGL
              style={{ width: '100%', height: '800px' }}
              mapStyle='mapbox://styles/mapbox/dark-v9'
              accessToken={TOKEN}
              onViewportChange={viewport => this.setState({ viewport })}
              {...this.state.viewport}
            >
              <Source id='route' type='geojson' data={this.state.data} />
              <Layer
                id='route'
                type='line'
                source='route'
                layout={{
                  'line-join': 'round',
                  'line-cap': 'round'
                }}
                paint={{
                  'line-color': 'red',
                  'line-width': 5
                }}
              />
            </MapGL>
      );
    }
}