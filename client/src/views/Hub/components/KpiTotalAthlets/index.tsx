import React, { Component, Fragment } from "react";
import { Typography, Paper } from "@material-ui/core";

export interface Props {}

export default class FilterControl extends Component {
  constructor({}: Props) {
    super({});
    this.state = {};
  }
  render() {
    return (
      <Fragment>
          <Paper elevation={3}>
          <Typography variant="h3">KPI: Total Athlets Preview</Typography>
          </Paper>        
      </Fragment>
    );
  }
}
