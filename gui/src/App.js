import React, { Component } from 'react';
import { Nav, Navbar, NavItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
// we use a HashRouter so file:// scheme will work
import { HashRouter, Redirect, Route, Switch } from 'react-router-dom';
import 'jstree/dist/themes/default/style.min.css';

import { JS_TREE_CONF } from './config.js';
import AwsIFileInput from './file-input';
import AwsIHomeArea from './home-area';
import AwsIHelpArea from './help-area';
import AwsIInventoryArea from './inventory-area';
import './App.css';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      runDate: undefined,
      commandLine: undefined,
      version: undefined,
      botocoreVersion: undefined,
      showHelp: false,
      treeConf: undefined
    };
    this.awsInvData = undefined;
  }

  handleFileSelect = (evt) => {
    const file = evt.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      let parsed = JSON.parse(reader.result);
      this.handleAwsInvData(parsed);
    };
    reader.readAsText(file);
  };

  handleAwsInvData = (data) => {
    this.setState({
      runDate: data.run_date,
      commandLine: data.commandline,
      version: data.version,
      botocoreVersion: data.botocore_version,
      treeConf: this.buildJsTreeConf(data.responses),
    });
  };

  buildJsTreeConf(responses) {
    const extra_conf = {
      core: {data: responses}
    }
    return {...JS_TREE_CONF, ...extra_conf};
  }

  handleNavHelp = () => {
    this.setState({showHelp: ! this.state.showHelp});
  };

  renderHomeContent = () => {
    return (
      this.state.treeConf === undefined ? (
        <AwsIFileInput onFileSelect={this.handleFileSelect} />
      ) : (
        <AwsIHomeArea
          runDate={this.state.runDate}
          commandLine={this.state.commandLine}
          version={this.state.version}
          botocoreVersion={this.state.botocoreVersion}
        />
      )
    );
  };

  renderInventoryContent = () => {
    return (
      this.state.treeConf === undefined ? <Redirect to="/" /> : <AwsIInventoryArea treeConf={this.state.treeConf} />
    );
  };

  render() {
    return (
      <div className="App">
        <HashRouter>
          <div>
            <Navbar inverse>
              <Navbar.Header>
                <Navbar.Brand>
                  AWS Inventory
                </Navbar.Brand>
                <Navbar.Toggle />
              </Navbar.Header>
              <Navbar.Collapse>
                <Nav>
                  <LinkContainer exact to="/"><NavItem>Home</NavItem></LinkContainer>
                  <LinkContainer to="/inventory"><NavItem disabled={this.state.treeConf === undefined}>Inventory</NavItem></LinkContainer>
                  <NavItem
                    eventKey={3}
                    target="_blank"
                    rel="noopener noreferrer"
                    href="https://github.com/nccgroup/aws-inventory"
                  >
                    About
                  </NavItem>
                  <NavItem onSelect={this.handleNavHelp}>Help</NavItem>
                </Nav>
              </Navbar.Collapse>
            </Navbar>

          <AwsIHelpArea show={this.state.showHelp} onHide={this.handleNavHelp} />

          <Switch>
            <Route exact path="/" render={this.renderHomeContent} />
            <Route path="/inventory" render={this.renderInventoryContent} />
          </Switch>

          </div>
        </HashRouter>
      </div>
    );
  }
}

export default App;
