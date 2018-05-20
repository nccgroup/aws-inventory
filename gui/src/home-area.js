import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Jumbotron } from 'react-bootstrap';


export default class AwsIHomeArea extends Component {
  render() {
    return (
      <div className="container">
        <Jumbotron>
          <h3>run date: <small>{this.props.runDate}</small></h3>
          <h3>commandline: <small>{this.props.commandLine}</small></h3>
          <h3>version: <small>{this.props.version}</small></h3>
          <h3>botocore version: <small>{this.props.botocoreVersion}</small></h3>
        </Jumbotron>        
      </div>
    );
  }
}

AwsIHomeArea.propTypes = {
  runDate: PropTypes.string,
  commandLine: PropTypes.string,
  version: PropTypes.string,
  botocoreVersion: PropTypes.string
};