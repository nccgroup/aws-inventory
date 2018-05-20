import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { ButtonGroup, DropdownButton, Glyphicon, MenuItem } from 'react-bootstrap';

import AwsISearch from './search';


export default class AwsIToolbar extends Component {
  render() {
    return (
      <div>
        <ButtonGroup>
          <DropdownButton title="Options" id="options">
            <MenuItem
              eventKey="showExtraNodes"
              onSelect={this.props.onSelect}
            >
              {this.props.preferences.showExtraNodes ? <span><Glyphicon glyph="ok" /> </span>: null}
              Show extra nodes (metadata and empty)
            </MenuItem>
          </DropdownButton>
          <AwsISearch onChange={this.props.onSearch} />
        </ButtonGroup>
      </div>
    );
  }
}

AwsIToolbar.propTypes = {
  onSelect: PropTypes.func,
  preferences: PropTypes.object,
  onSearch: PropTypes.func
};