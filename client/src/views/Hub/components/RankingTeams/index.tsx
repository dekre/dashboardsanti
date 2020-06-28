import React, { Component, Fragment } from "react";
import { Typography, Paper } from "@material-ui/core";
import Skeleton from "@material-ui/lab/Skeleton";

export interface Props {}

export default class ViewComponent extends Component {
  constructor({}: Props) {
    super({});
    this.state = {};
  }
  render() {
    return (
      <Fragment>
        <Paper elevation={3} style={{ padding: 12 }}>
          <Typography variant="h6">Ranking - Top Teams</Typography>
          <Skeleton variant="text" />
          <Skeleton variant="circle" width={40} height={40} />
          <Skeleton variant="rect" height={240} />
        </Paper>
      </Fragment>
    );
  }
}
