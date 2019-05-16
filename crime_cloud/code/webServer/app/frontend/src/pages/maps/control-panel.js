import React, {PureComponent} from 'react';
import './map.css';

const defaultContainer = ({children}) => <div className="control-panel">{children}</div>;

export default class ControlPanel extends PureComponent {
  render() {
    const Container = this.props.containerComponent || defaultContainer;
    const {settings} = this.props;

    return (
      <Container>
        <h3>Interactive GeoJSON</h3>
        <p>
          Map showing total offence event by district in year <b className="control_panel_year">{settings.year}</b>. Hover over a
          district to see details.
        </p>
        <hr />

        <div key={'year'} className="input">
          <label>Year</label>
          <input
            type="range"
            value={settings.year}
            min={2015}
            max={2017}
            step={1}
            onChange={evt => this.props.onChange('year', evt.target.value)}
          />
        </div>
      </Container>
    );
  }
}
