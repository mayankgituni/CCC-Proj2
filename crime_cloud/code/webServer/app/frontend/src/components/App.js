import React from 'react';
import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';

import themes, { overrides } from '../themes';
import Layout from './Layout';
import Error from '../pages/error';

const theme = createMuiTheme({...themes.default, ...overrides});

const PrivateRoute = ({ component, ...rest }) => {
  return (
    <Route
      {...rest} render={props => (
        React.createElement(component, props)
    )}
    />
  );
};

// const PublicRoute = ({ ...rest }) => {
//   return (
//     <Route
//       {...rest} render={props => (
//         <Redirect
//           to={{
//             pathname: '/',
//           }}
//         />
//       ) 
//     }
//     />
//   );
// };

const App = () => (
  <MuiThemeProvider theme={theme}>
    <BrowserRouter>
      <Switch>
        <Route exact path="/" render={() => <Redirect to="/app/dashboard" />} />
        <Route exact path="/app" render={() => <Redirect to="/app/dashboard" />} />
        <PrivateRoute path="/app" component={Layout} />
        {/* <PublicRoute path="/"  /> */}
        <Route component={Error} />
      </Switch>
    </BrowserRouter>
  </MuiThemeProvider>
);

export default App;