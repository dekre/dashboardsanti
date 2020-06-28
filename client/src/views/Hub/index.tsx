import React, { Component, Fragment } from "react";
import { Grid, Typography } from "@material-ui/core";
import {
  FilterControl,
  KpiTotalAthlets,
  RankingAthlets,
  RankingTeams,
  SeasonPerformance,
  TrainingOverview,
} from "./components";

export interface Props {}

export default class HubView extends Component {
  constructor({}: Props) {
    super({});
    this.state = {};
  }
  render() {
    return (
      <Fragment>
        <div style={{ padding: 24 , marginLeft: 72}}>
          <Grid container justify="center" spacing={4}>
            <Grid item lg={6} xs={12}>
              <FilterControl />
            </Grid>
            <Grid item lg={6} xs={12}>
              <KpiTotalAthlets />
            </Grid>
            <Grid item lg={6} xs={12}>
              <RankingAthlets />
            </Grid>
            <Grid item lg={6} xs={12}>
              <RankingTeams />
            </Grid>
            <Grid item lg={6} xs={12}>
              <SeasonPerformance />
            </Grid>
          </Grid>
        </div>
      </Fragment>
    );
  }
}
