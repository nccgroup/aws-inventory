import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { ListGroup, ListGroupItem, Modal } from 'react-bootstrap';


export default class AwsIHelpArea extends Component {
  render() {
    return (
      <Modal show={this.props.show} keyboard={true} onHide={this.props.onHide} >
        <Modal.Body>
          <ListGroup>
            <ListGroupItem active><h4>Help</h4></ListGroupItem>
            <ListGroupItem>
              Icon Legend
              <div>
                <span className="glyphicon glyphicon-home"></span>: root node,
                <span className="glyphicon glyphicon-cloud"></span>: service,
                <span className="glyphicon glyphicon-globe"></span>: region,
                <span className="glyphicon glyphicon-play"></span>: operation,
                <span className="glyphicon glyphicon-stop"></span>: leaf node
              </div>
            </ListGroupItem>
            <ListGroupItem>Right-click: context menu</ListGroupItem>
            <ListGroupItem>Double-click: expand node</ListGroupItem>
            <ListGroupItem><kbd>Home</kbd>: focus root node</ListGroupItem>
            <ListGroupItem><kbd>End</kbd>: focus deepest expanded node</ListGroupItem>
            <ListGroupItem><kbd>←</kbd> <kbd>→</kbd> <kbd>↑</kbd> <kbd>↓</kbd>: move/expand/collapse nodes</ListGroupItem>
            <ListGroupItem>Operations with no response data are hidden. Hover over region nodes to see number of hidden operations.</ListGroupItem>
            <ListGroupItem>The number in parentesis after operations is the number of non-empty responses.</ListGroupItem>
          </ListGroup>
        </Modal.Body>
      </Modal>
    );
  }
}

AwsIHelpArea.propTypes = {
  show: PropTypes.bool,
  onHide: PropTypes.func
};