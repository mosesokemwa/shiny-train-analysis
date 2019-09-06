import React from "react";
import JobAnalytics from "./components/JobAnalytics";
import Layout from "./components/layout";
import {Provider} from "react-redux";
import {Route, Router, Switch} from "react-router-dom";
import {store} from "./store";
import {createBrowserHistory} from "history";
import {FireWall, OAuthResponse} from "./components/authentication";

export default class App extends React.Component {
    render() {
        return (
            <Provider store={store}>
                <Router history={createBrowserHistory()}>
                    <Route component={OAuthResponse} path='/oauth/:service/response' />
                    <FireWall>
                        <Layout>
                            <Switch>
                                {/*<Route component={DashBoard} path='/' exact />*/}
                                <Route component={JobAnalytics} path='/jobs/:jobId?' />
                                {/*<Route component={Companies} path='/companies/' />*/}
                                {/*<Route component={Statistics} path='/statistics/' />*/}
                            </Switch>
                        </Layout>
                    </FireWall>
                </Router>
            </Provider>
        )
    }
}