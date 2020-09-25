import React, { Component, Fragment } from "react";
import { Grid, Typography } from "@material-ui/core";
import {
  KpiDataValidation,
  KpiPerformance,
  RankingAthlets,
  RankingTeams,
  SeasonPerformance,
  TeamStructure,
  TrainingOverview,
  SummaryDetails,
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
        <Grid container justify="center" spacing={4}>
          <Grid item xs={3}>
            <
               />
          </Grid>
          <Grid item  xs={3}>
            <KpiPerformance />
          </Grid>
          <Grid item  xs={6}>
            <TrainingOverview />
          </Grid>          
          <Grid item  xs={6}>
            <SeasonPerformance />
          </Grid>
          <Grid item  xs={3}>
            <RankingAthlets />
          </Grid>
          <Grid item  xs={3}>
            <RankingTeams />
          </Grid>
          <Grid item  xs={8}>
            <SummaryDetails />
          </Grid>
          <Grid item  xs={4}>
            <TeamStructure />
          </Grid>
        </Grid>
      </Fragment>
    );
  }
}
