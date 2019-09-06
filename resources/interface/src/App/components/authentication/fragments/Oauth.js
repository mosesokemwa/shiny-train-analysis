import CanvasLogo from "../../../assets/CanvasLogo.png";
import GoogleLogo from "../../../assets/GoogleLogo.png";
import React, {Component} from "react";
import {connect} from "react-redux";
import * as loginActions from "../actions";

export class CanvasOauth extends Component{
    static getOauthUrl(next){
        const url = new URL("/oauth/canvas/response", document.URL);
        const urlParams = {
            "redirect_uri": url.toString(),
            "response_type": "code",
            "client_id": process.env.REACT_APP_CANVAS_API_CLIENT_KEY
        };
        if(next){
            urlParams["state"] = JSON.stringify({"next": next})
        }
        const params = new URLSearchParams();
        Object.entries(urlParams).map(([key, value]) => params.append(key, value));
        return "https://moringaschool.instructure.com/login/oauth2/auth?" + params;
    }
    render() {
        return (
            <div className='text-center p-2 pointer mt-2'>
                <a
                    style={{color: 'inherit'}}
                    className='border font-weight-bold d-inline-block shadow-sm rounded shadow-hover text-decoration-none'
                    href={CanvasOauth.getOauthUrl(this.props.next)}>
                    <div style={{height: 38, width: 39}} className='d-inline-block p-2 border-right'>
                        <img src={CanvasLogo}  alt='Canvas' height='100%'/>
                    </div>
                    <span className='p-3'>Sign In With Canvas</span>
                </a>
            </div>
        );
    }
}

export class GoogleOauth extends Component{
    static getOauthUrl(next){
        const url = new URL("/oauth/google/response", document.URL);
        const urlParams = {
            "redirect_uri": url.toString(),
            "response_type": "code",
            "scope": "openid email profile",
            "client_id": process.env.REACT_APP_GOOGLE_API_CLIENT_KEY
        };
        if(next){
            urlParams["state"] = JSON.stringify({"next": next})
        }
        const params = new URLSearchParams();
        Object.entries(urlParams).map(([key, value]) => params.append(key, value));
        return "https://accounts.google.com/o/oauth2/v2/auth?" + params;
    }
    render() {
        return (
            <div className='text-center p-2 pointer mt-2'>
                <a
                    style={{color: 'inherit'}}
                    className='border font-weight-bold d-inline-flex shadow-sm rounded shadow-hover text-decoration-none'
                    href={GoogleOauth.getOauthUrl(this.props.next)}>
                    <div className='border-right d-inline-flex align-items-center'>
                        <img src={GoogleLogo}  alt='G'/>
                    </div>
                    <span className='p-3'>
                        Sign In With Google
                        <div className='small border-top'><b>@moringaschool.com</b> only</div>
                    </span>
                </a>
            </div>
        );
    }
}

class AuthResponse extends Component{
    componentDidMount() {
        const {service} = this.props.match.params;
        const {search} = this.props.location;
        const params = new URLSearchParams(search);
        if (params.has('code')){
            const code = params.get('code');
            this.props.post(service, code);
        }
        if (params.has('state')){
            let redirection = '/';
            try {
                const state = JSON.parse(params.get('state'));
                if (state['next']){
                    redirection = state['next'];
                }
            } catch (e) {
                console.log("Error", e)
            }
            this.props.history.replace(redirection)
        }
    }

    render() {
        return <span/>
    }
}

function mapStateToProps(state) {
    return {
        isLoading: state.authentication.isLoading
    }
}

export const OAuthResponse = connect(mapStateToProps, loginActions)(AuthResponse);