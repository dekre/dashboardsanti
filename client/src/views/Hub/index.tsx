import React, { Component, Fragment } from "react";
import { Grid, Typography } from "@material-ui/core";

export interface Props {}

export default class HubView extends Component {
  constructor({}: Props) {
    super({});
    this.state = {};
  }
  render() {
    return (
      <Fragment>
        <div style={{ padding: 24 }}>
          <Grid container justify="center" spacing={4}>
            <Grid item lg={6} xs={12}>
              <div style={{ padding: 24 }}>
                <Typography variant="h1">Hub Preview</Typography>
                <Typography variant="subtitle2">
                  Under construction...top secret development, do not tell
                  anyone!
                </Typography>
              </div>
            </Grid>
          </Grid>
        </div>
      </Fragment>
    );
  }
}
