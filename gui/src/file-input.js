import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { ControlLabel, FormControl } from 'react-bootstrap';


export default class AwsIFileInput extends Component {
  render() {
    return (
      <div className="container">
        <ControlLabel>Select data file (from commandline tool).</ControlLabel>
        <FormControl
          type="file"
          accept=".json, application/json"
          onChange={this.props.onFileSelect}
          id="file"
        />
      </div>
    );
  }
}

AwsIFileInput.propTypes = {
  onFileSelect: PropTypes.func
};