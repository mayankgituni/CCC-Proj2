import React, {Component} from 'react';
import {render} from 'react-dom';
import MapGL, {NavigationControl, FlyToInterpolator} from 'react-map-gl';
import ControlPanel from './control-panel';
import Button from '@material-ui/core/Button';
import {defaultMapStyle, dataLayer} from './map-style.js';
import {updatePercentiles} from './utils';
import {fromJS} from 'immutable';
import Axios from 'axios';
import './map.css';
import PropTypes from 'prop-types';

import Loader from './loader';

import ChartModal from './CustomModal'

const MAPBOX_TOKEN = 'pk.eyJ1IjoidG91Y2h3b29kIiwiYSI6ImNqdms4MnpiNjA5YWI0YW9kdnRobHZhangifQ.dLTyBQp4CkPvN27MZC1qcg'; // Set your mapbox token here


export default class App extends Component {

  state = {
    isFetching:false,
    mapStyle: defaultMapStyle,
    modalVisible: false,
    year: 2015,
    total_offence: 0,
    districtName: null,
    clickedData: null,
    data: null,
    data_2015: null,
    data_2016: null,
    data_2017: null,
    data_sydn: null,
    hoveredFeature: null,
    viewport: {
      latitude: -37.713179,
      longitude: 145.250259,
      zoom: 3,
      bearing: 0,
      pitch: 0
    },
  };

  componentWillMount() {
    this.setState({isFetching:true})

    Axios.get(`http://localhost:50000/melb/2015 `) // JSON File Path
    // Axios.get(`http://`) // JSON File Path
    
    .then( response => {
        this.setState({data_2015:response.data})
        this.setState({data:this.state.data_2015})
        console.log(`2015: `, response.data)
        this._loadData(this.state.data);
        this.setState({isFetching:false})
    })

    .catch(function (error) {
      console.log(error);
    });


    Axios.get(`http://localhost:50000/melb/2016`) // JSON File Path

    .then( response => {
        this.setState({data_2016:response.data})
        console.log(`2016: `, response.data)
    })

    .catch(function (error) {
      console.log(error);
    });


    Axios.get('http://localhost:50000/melb/2017') // JSON File Path

    .then( response => {
        this.setState({data_2017:response.data})
        console.log('2017: ', response.data)
    })

    .catch(function (error) {
      console.log(error);
    });


    Axios.get('http://localhost:50000/sydn') // JSON File Path

    .then( response => {
        this.setState({data_sydn:response.data})
        console.log('sydn: ', this.state.data_sydn)
        this._loadData(response.data);
    })

    .catch(function (error) {
      console.log(error);
    });


  }

  componentDidMount() {

  }

  _loadData = (data) => {

    console.log('load data: ', data)
    
    updatePercentiles(data, f => f.properties.total_offence);
    
    const mapStyle = defaultMapStyle
      // Add geojson source to map
      .setIn(['sources', 'crimeRateBySuburb'], fromJS({type: 'geojson', data}))
      // Add point layer to map
      .set('layers', defaultMapStyle.get('layers').push(dataLayer));

    this.setState({data, mapStyle});

  };

  _updateSettings = (name, value) => {

    // console.log(name, value)
    if (name === 'year') {

      this.setState({year: value});

      const {mapStyle} = this.state;

      let data = {}

      if(value === '2015'){
        data = this.state.data_2015
      } else if(value === '2016'){
        data = this.state.data_2016
      } else if(value === '2017') {
        data = this.state.data_2017
      }

      if (data) {
        console.log(data)
        updatePercentiles(data, f => f.properties.total_offence);
        const newMapStyle = mapStyle.setIn(['sources', 'crimeRateBySuburb'], fromJS({type: 'geojson', data}))
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

  _onClickEvent = event => {
    const {
      features
    } = event;
    const districtData = features && features.find(f => f.layer.id === 'data');

    // this.setState({hoveredFeature, x: offsetX, y: offsetY});

    // const {hoveredFeature} = this.state;

    let data = []
    let districtName = ''
    let lga_erp = 0

    if(districtData && districtData.properties) {
      var obj = districtData.properties
      for (var k in obj) {
        if (k === 'lga_name11' || k === 'lga_code' || k === 'lga_erp' || 
            k === 'total_offence' || k === 'percentile' || k === 'value'){}
        else{
          const tmp = {
            'name': k,
            'value': obj[k]
          }
          data.push(tmp)
        }
      }

      districtName = districtData.properties.lga_name11
      lga_erp = districtData.properties.lga_erp
    }

    this.setState({ 
      modalVisible: true,
      clickedData: data,
      districtName: districtName ,
      total_offence: districtData.properties.total_offence
    });
  };

  handleModal = (type, selectedData) => {
    if (type === 'cancel') {
      this.setState({
        modalVisible: false,
        selectedData: undefined,
      });
    } 
    else if (type === 'ok') {
      this.setState({
        modalVisible: false,
        selectedData: undefined,
      });
    }  
  }

  _goToSYD = () => {
      const viewport = {
          ...this.state.viewport,
          latitude: -33.865143,
          longitude: 151.2099,
          zoom: 8,
          transitionDuration: 3000,
          transitionInterpolator: new FlyToInterpolator(),
      };
      this.setState({viewport});
      this._loadData(this.state.data_sydn);
      console.log('state sydney: ', this.state.data_sydn)
  };

  _renderTooltip() {
    const {hoveredFeature, x, y} = this.state;

    let data = []
    let districtName = ''
    let lga_erp = 0

    if(hoveredFeature && hoveredFeature.properties) {
      var obj = hoveredFeature.properties
      for (var k in obj) {
        if (k === 'lga_code' || k === 'lga_erp' || k === 'total_offence' || k === 'percentile' || k === 'value'){}
        else{
          const tmp = {
            'name': k,
            'value': obj[k]
          }
          data.push(tmp)
        }
      }

      districtName = hoveredFeature.properties.lga_name11
      lga_erp = hoveredFeature.properties.lga_erp
    }
    

    return (
      hoveredFeature && (
        <div className="tooltip" style={{left: x, top: y}}>
          <div>District: {hoveredFeature.properties.lga_name11}</div>
          <div>Total offence count: {hoveredFeature.properties.total_offence}</div>
          <div>LGA ERP: {hoveredFeature.properties.lga_erp}</div>
          <div>Crime Rate: {(hoveredFeature.properties.total_offence / hoveredFeature.properties.lga_erp) * 100}</div>
        </div>
        
      )
    );
  }

  render() {
    const {viewport, mapStyle} = this.state;

    return (
      
      <div style={{height: '100%'}}>
        <ChartModal
          modalOpen={this.state.modalVisible}
          setModalData={this.handleModal}
          data={this.state.clickedData}
          districtName={this.state.districtName}
          totalOffence={this.state.total_offence}
        />
        <Button onClick={this._goToSYD} color="primary">Go to Sydney</Button>
        {this.state.isFetching &&
          <Loader/>
        }
        <MapGL
          {...viewport}
          width="100%"
          height={800}
          mapStyle={mapStyle}
          onViewportChange={this._onViewportChange}
          mapboxApiAccessToken={MAPBOX_TOKEN}
          onHover={this._onHover}
          onClick={this._onClickEvent}
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
