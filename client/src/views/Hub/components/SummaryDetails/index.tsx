import React, { Component, Fragment } from "react";
import {
  Typography,
  Paper,
  Card,
  CardHeader,
  CardMedia,
  CardContent,
  CardActions,
  IconButton,
} from "@material-ui/core";
import MoreVertIcon from "@material-ui/icons/MoreVert";
import clsx from "clsx";
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
        <Card elevation={3}>
          <CardHeader
            action={
              <IconButton aria-label="settings">
                <MoreVertIcon />
              </IconButton>
            }
            title={<Typography variant="h6">Summary Details</Typography>}
          />
          <CardContent>
            <Skeleton variant="text" />
            <Skeleton variant="circle" width={40} height={40} />
            <Skeleton variant="rect" height={240} />
          </CardContent>
        </Card>
      </Fragment>
    );
  }
}
