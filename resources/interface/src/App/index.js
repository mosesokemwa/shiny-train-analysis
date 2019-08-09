import React from "react";
import JobAnalytics from "./components/JobAnalytics";
import Layout from "./components/layout";
import {Provider} from "react-redux";
import {Route, Router, Switch} from "react-router-dom";
import {store} from "./store";
import {createBrowserHistory} from "history";

export default class App extends React.Component {
    render() {
        return (
            <Provider store={store}>
                <Router history={createBrowserHistory()}>
                    <Layout>
                        <Switch>
                            {/*<Route component={DashBoard} path='/' exact />*/}
                            <Route component={JobAnalytics} path='/jobs/' />
                            {/*<Route component={Companies} path='/companies/' />*/}
                            {/*<Route component={Statistics} path='/statistics/' />*/}
                        </Switch>
                    </Layout>
                </Router>
            </Provider>
        )
    }
}