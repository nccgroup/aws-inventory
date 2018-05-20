import PropTypes from 'prop-types';
import React, { Component } from 'react';
import $ from 'jquery';
import 'jstree';


export default class ReactJsTree extends Component {
  constructor(props) {
    super(props);
    this.state = {
      ready: false,
    };

    this.hidden_node_ids = [];  // track hidden nodes

    this.handleOpenNode = this.handleOpenNode.bind(this);
  }

  componentDidMount() {
    this.$el = $(this.el);
    this.renderJsTree(this.props.treeConf);
  }

  shouldComponentUpdate(nextProps, nextState) {
    /* make sure jstree is ready first */

    if (!this.state.ready) {
      return false;
    }

    let inst = this.$el.jstree(true);

    /* handle search */

    if (nextProps.searchString) {
      inst.search(nextProps.searchString);
    }
    else {
      inst.clear_search();
    }
    
    if (this.props.preferences.showExtraNodes !== nextProps.preferences.showExtraNodes) {
      this.toggle_metadata_viz(inst);
    }
    
    // never let React update the DOM node for jstree instance
    return false;
  }

  componentWillUnmount() {
    this.setState({ready: false});
    this.$el.jstree(true).destroy();
    this.$el = null;
  }

  handleOpenNode(evt, data) {
    const inst = data.instance,
        obj = data.node;

    /* walk node's children so we can handle leaf and metadata nodes */

    for (let i = 0; i < obj.children.length; i++) {
        const child = inst.get_node(obj.children[i]);
        if (child.type === 'response_metadata') {
            if (!this.props.preferences.showExtraNodes) {
              // hide the response metadata nodes
              inst.hide_node(child);
            }
        }
        else if (inst.is_leaf(child)) {
            // set "leaf" node type
            inst.set_type(child, 'leaf');
        }
    }
  }
  
  renderJsTree(treeConf) {
    this.$el.on('open_node.jstree', this.handleOpenNode).on('ready.jstree', (evt, data) => {
      this.setState({ready: true});
    }).jstree(treeConf);
  }
    
  toggle_metadata_viz(inst) {
    if (this.hidden_node_ids.length > 0) {
        this.hidden_node_ids.forEach(function(node_id, index, array) {
            inst.hide_node(node_id);
        });
        this.hidden_node_ids = [];
    }
    else {
        this.hidden_node_ids = inst.show_all();
    }
  } 
  
  render() {
    return (
      <div ref={el => this.el = el}></div>
    );
  }
}

ReactJsTree.propTypes = {
  treeConf: PropTypes.object,
  preferences: PropTypes.object
};