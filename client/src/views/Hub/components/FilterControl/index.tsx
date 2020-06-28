import React, { Component, Fragment } from "react";
import { Grid, Typography, Paper } from "@material-ui/core";

export interface Props {}

export default class ViewComponent extends Component {
  constructor({}: Props) {
    super({});
    this.state = {};
  }
  render() {
    return (
      <Fragment>
          <Paper elevation={3}>
          <Typography variant="h3">Filter Conotrol Preview</Typography>
          </Paper>        
      </Fragment>
    );
  }
}
