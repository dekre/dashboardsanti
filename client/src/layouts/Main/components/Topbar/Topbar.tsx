import React from "react";
import { Link as RouterLink } from "react-router-dom";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import {
  AppBar,
  Toolbar,
  IconButton,
  Button,
  Typography,
  List,
  ListItem,
  Divider,
  ListItemText,
  ListItemIcon,
  Drawer,
} from "@material-ui/core";
import ZooIcon from "@material-ui/icons/List";
import DashboardIcon from '@material-ui/icons/Dashboard';
import MenuIcon from "@material-ui/icons/Menu";
import HubIcon from "@material-ui/icons/DeviceHub";
import SettingsIcon from "@material-ui/icons/Settings";

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  hide: {
    display: 'none',
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
  },
  drawerOpen: {
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerClose: {
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: theme.spacing(7) + 1,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(9) + 1,
    },
  },
  toolbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  alignItemsAndJustifyContent: {
    display: 'none',
    [theme.breakpoints.up('md')]: {
      display: 'flex',
    },
  },
}));

export interface Props {
  className: any;
  onSidebarOpen: any;
  rest?: any;
}

const Topbar = ({ className, onSidebarOpen, rest }: Props) => {
  const classes = useStyles();
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <div className={classes.root}>
      <AppBar
        {...rest}
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open,
        })}
        style={{ background: "#002897" }}
      >
        <Toolbar>
          <IconButton
            edge="start"
            aria-label="open drawer"
            onClick={handleDrawerOpen}            
            className={clsx(classes.menuButton, {
              [classes.hide]: open,
            })}
            color="inherit"
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6">
            Santi's App
          </Typography>
          <div className={classes.alignItemsAndJustifyContent} />
          <div className={classes.content} />
          <div className={classes.menuButton} />
          <Button color="inherit" startIcon={<HubIcon />} href="/hub">
            Hub
          </Button>
          <div className={classes.menuButton} />
          <Button color="inherit" startIcon={<ZooIcon />} href="/hub">
            Data
          </Button>
          <div className={classes.menuButton} />
          <Button color="inherit" startIcon={<SettingsIcon />} href="/hub">
            Settings
          </Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        className={clsx(classes.drawer, {
          [classes.drawerOpen]: open,
          [classes.drawerClose]: !open,
        })}
        classes={{
          paper: clsx({
            [classes.drawerOpen]: open,
            [classes.drawerClose]: !open,
          }),
        }}
      >
        <div className={classes.toolbar}>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "rtl" ? (
              <DashboardIcon />
            ) : (
              <DashboardIcon />
            )}
          </IconButton>
        </div>        
      </Drawer>
    </div>
  );
};

Topbar.propTypes = {
  className: PropTypes.string,
  onSidebarOpen: PropTypes.func,
};

export default Topbar;
