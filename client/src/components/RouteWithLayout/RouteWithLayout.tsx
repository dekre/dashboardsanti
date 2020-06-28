import React from 'react';
import { Route } from 'react-router-dom';
import PropTypes from 'prop-types';

export interface Props {
  layout: any;
  component: any;
  rest?: any;
}

const RouteWithLayout = ({layout, component, rest}: Props) => {  
  let Layout = layout;
  let Component = component;

  return (
    <Route
      exact
      {...rest}
      render={matchProps => (
        <Layout>
          <Component {...matchProps} />
        </Layout>
      )}
    />
  );
};

RouteWithLayout.propTypes = {
  component: PropTypes.any.isRequired,
  layout: PropTypes.any.isRequired,
  path: PropTypes.string
};

export default RouteWithLayout;
