import PropTypes from 'prop-types';
import { FormControl, InputGroup } from 'react-bootstrap';
import React, { Component } from 'react';


export default class AwsISearch extends Component {

  handleClearSearch = (evt) => {
    this.inputRef.value = '';
    this.props.onChange(evt);
  }

  render() {
    return (
      <InputGroup>
        <FormControl
          type="text"
          placeholder="Search"
          inputRef={input => this.inputRef = input}
          onChange={this.props.onChange}
        />
        <span
          className="navbar-form input-group-addon glyphicon glyphicon-remove-circle"
          aria-hidden="true"
          style={{top: '0px'}}
          onClick={this.handleClearSearch}
        />
      </InputGroup>
    );
  }
}

AwsISearch.propTypes = {
  onChange: PropTypes.func
};