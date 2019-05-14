import React, {PureComponent} from 'react';

const defaultContainer = ({children}) => <div className="control-panel">{children}</div>;

export default class ControlPanel extends PureComponent {
  render() {
    const Container = this.props.containerComponent || defaultContainer;
    const {settings} = this.props;

    return (
      <Container>
        <h3>Interactive GeoJSON</h3>
        <p>
          Map showing median household income by state in year <b>{settings.year}</b>. Hover over a
          state to see details.
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
