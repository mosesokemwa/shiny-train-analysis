import React, {Component} from "react";
import {connect} from "react-redux";
import AuthPage from "./fragments/AuthPage";
import * as authActions from "./actions"

class FireWall extends Component{
    static defaultProps = {
        full: true,
    };
    static loaded = false;

    componentDidMount() {
        if (!FireWall.loaded){
            FireWall.loaded = true;
            this.props.get()
        }
    }

    render() {
        const {isLoading, isAuthenticated, full, checkRole, user, method} = this.props;
        const {pathname, search} = window.location;
        const next = pathname + search;
        if(isLoading || !FireWall.loaded){
            return (
                <div className={'d-flex align-items-center justify-content-center ' + (full?'vh-100 vw-100':'')}>
                    <div className='spinner-border spinner text-primary' style={{width: '40px', height: '40px'}}/>
                </div>
            )
        }
        let isAuthorised = true;
        if (checkRole){
            isAuthorised = user['roles'].includes(checkRole);
        }
        return (
            <div>
                {(isAuthenticated && isAuthorised)?(this.props.children):<AuthPage full={full} next={next} method={method}/>}
            </div>
        );
    }
}
export default connect(state => ({
    user: state.authentication.user,
    isLoading: state.authentication.isLoading,
    isAuthenticated: state.authentication.isAuthenticated
}), authActions)(FireWall)