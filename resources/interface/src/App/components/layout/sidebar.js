import React from "react";
import {NavLink} from "react-router-dom";
import {connect} from "react-redux";
import fetchProviders from "../../actions/fetchProviders";
import "./sidebar.css";
import fetchSync from "../../actions/fetchSync";
import moment from "moment";

const styles = {
    sideBar: {
        position: 'fixed',
        top: 0,
        bottom: 0,
        left: 0
    }
};

class SideBar extends React.Component{
    componentDidMount() {
        this.props.fetchProviders();
        this.props.fetchSync();
    }

    render() {
        const {providers, sync} = this.props;
        return (
            <nav className='sidebar navbar navbar-dark vh-100 bg-dark col-lg-2 col-1' style={styles.sideBar}>
                <ul className="navbar-nav mb-auto w-100 text-center text-lg-left">
                    <li className="nav-item">
                        <NavLink className="nav-link" to="/" exact>
                            <i className='fa fa-home'/>
                            <span className='d-none d-lg-inline'>&nbsp;Home</span>
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <div className="nav-link">
                            <i className='fa fa-list'/>
                            <span className='d-none d-lg-inline'>&nbsp;Jobs</span>
                            <ul className='d-none d-lg-block provider-nav'>
                                <li className='nav-item'>
                                    <NavLink className="nav-link" to="/jobs/" exact>
                                        <span className='d-none d-lg-inline'>All Jobs</span>
                                    </NavLink>
                                </li>
                                {providers.map(provider =>(
                                    <li className='nav-item' key={provider.id}>
                                        <NavLink className="nav-link" to={`/jobs/${provider.id}`} exact>
                                            <span className='d-none d-lg-inline'>{provider.name} <span className='text-white-50'>({provider.job_count})</span></span>
                                        </NavLink>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </li>
                    <li className="nav-item">
                        <NavLink className="nav-link" to="/companies/">
                            <i className='fa fa-building'/>
                            <span className='d-none d-lg-inline'>&nbsp;Companies</span>
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink className="nav-link" to="/statistics/">
                            <i className='fa fa-area-chart'/>
                            <span className='d-none d-lg-inline'>&nbsp;Statistics</span>
                        </NavLink>
                    </li>
                </ul>
                <div className='mt-auto text-white-50 small d-none d-md-block'>
                    Last updated
                    <div>
                        {moment(sync.created_at).format('D MMMM Y h:mm:ss A')}
                    </div>
                </div>
            </nav>
        );
    }
}

function mapStateToProps(state) {
    return {
        providers: state.providers.data,
        sync: state.sync.data
    }
}

export default connect(mapStateToProps, {fetchProviders, fetchSync})(SideBar)