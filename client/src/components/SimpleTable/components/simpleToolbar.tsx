import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import Tooltip from '@material-ui/core/Tooltip';

const useToolbarStyles = makeStyles(theme => ({
  root: {
    paddingLeft: theme.spacing(2),
    paddingRight: theme.spacing(1)
  },
  title: {
    flex: '1 1 100%'
  }
}));

export interface Props {
  title: string;
  onClick: any;
  actionIcon: any;
}

const SimpleTableToolbar = ({ title, onClick, actionIcon }: Props) => {
  const classes = useToolbarStyles();  
  const ActionIcon = actionIcon;

  return (
    <Toolbar className={clsx(classes.root)}>
      <Typography
        className={classes.title}
        component="div"
        id="tableTitle"
        variant="h6">
        {title}
      </Typography>

      <Tooltip title="Filter list">
        <IconButton aria-label="create project" onClick={onClick}>
          <ActionIcon />
        </IconButton>
      </Tooltip>
    </Toolbar>
  );
};

SimpleTableToolbar.propTypes = {
  // actionIcon: PropTypes.object,
  onClick: PropTypes.func,
  title: PropTypes.string
};

export default SimpleTableToolbar;
