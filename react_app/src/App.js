import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import "./index.css";
import Home from "./pages/Home";
import NoMatch from "./pages/NoMatch";
import 'bootstrap/dist/css/bootstrap.min.css';

class App extends Component {
  render() {
    return (
        <Router>
              <Switch>
                <Route exact path="/" component={Home} />
                <Route exact path="/nomatch" component={NoMatch} />
              </Switch>
        </Router>
    );
  }
}

export default App;