import PropTypes from 'prop-types';
import React, { Component } from 'react';

import AwsIInventoryToolbar from './inventory-toolbar';
import ReactJsTree from './react-js-tree';


export default class AwsIInventoryArea extends Component {
  constructor(props) {
    super(props);
    /*
    toolBarOpts: object of new/changed options to pass to ReactJsTree
    */
    this.state = {
      searchString: undefined,
      preferences: {showExtraNodes: false},
    };
  }

  handleSearch = (evt) => {
    this.setState({searchString: evt.target.value});
  }
  
  handleSelect = (key, evt) => {
    switch (key) {
      case 'showExtraNodes':
        this.setState({preferences: {[key]: !this.state.preferences[key]}});
        break;
      default:
        console.log(`Unrecognized option "${key}".`);
     }
  };

  render() {
    if (this.props.treeConf && this.props.treeConf.core.data.length) {
      return (
        <div>
          <AwsIInventoryToolbar
            onSelect={this.handleSelect}
            onSearch={this.handleSearch}
            preferences={this.state.preferences}
          />
          <ReactJsTree
            treeConf={this.props.treeConf}
            searchString={this.state.searchString}
            preferences={this.state.preferences}
          />
        </div>
      );
    }
    else {
      return null;
    }
  }
}

AwsIInventoryArea.propTypes = {
  treeConf: PropTypes.object
};