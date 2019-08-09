import React from "react";
import {NavLink} from "react-router-dom";

const styles = {
    sideBar: {
        position: 'fixed',
        top: 0,
        bottom: 0,
        left: 0
    }
};

export default class SideBar extends React.Component{
    render() {
        return (
            <nav className='navbar navbar-dark vh-100 bg-dark col-lg-2 col-1' style={styles.sideBar}>
                <ul className="navbar-nav mb-auto w-100 text-center text-lg-left">
                    <li className="nav-item">
                        <NavLink className="nav-link" to="/" exact>
                            <i className='fa fa-home'/>
                            <span className='d-none d-lg-inline'>&nbsp;Home</span>
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink className="nav-link" to="/jobs/">
                            <i className='fa fa-list'/>
                            <span className='d-none d-lg-inline'>&nbsp;Jobs</span>
                        </NavLink>
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
            </nav>
        );
    }
}