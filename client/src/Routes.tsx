import React from "react";
import { HashRouter, Switch, Redirect } from "react-router-dom";

import { RouteWithLayout } from "./components";
import { Main as MainLayout } from "./layouts";

import { Hub } from "./views";

const Routes = () => {
  return (
    <HashRouter>
      <Switch>
        <Redirect exact from="/" to="/hub" />
        <RouteWithLayout component={Hub} layout={MainLayout} path="/hub" />
        <Redirect to="/not-found" />
      </Switch>
    </HashRouter>
  );
};

export default Routes;
