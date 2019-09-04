import * as React from "react";
import MoringaLogo from "../../../assets/MoringaLogo.png"
import {GoogleOauth, CanvasOauth} from "./Oauth";

const styles = {
    loginView: {
        width: '300px',
        height: '100%',
        display: 'flex',
        alignItems: 'center'
    },
    loginOptions: {
        width: '100%'
    },
    loginChoices: {
        minHeight: '50%'
    }
};

class AuthPage extends React.Component{
    static defaultProps = {
        next: '/',
        method: 'all'
    };
    render() {
        const {full, next, method} = this.props;
        const google = <GoogleOauth next={next}/>;
        const canvas = <CanvasOauth next={next}/>;
        let Auth = <div/>;
        if (method === 'all'){
            Auth = <>{google}{canvas}</>
        }
        if (method === 'google'){
            Auth = google
        }
        if (method === 'canvas'){
            Auth = canvas
        }
        return (
            <div className={'bg-light d-flex align-items-center justify-content-center ' + (full?'vh-100 vw-100':'my-4 py-4')}>
                <div style={styles.loginView}>
                    <div style={styles.loginOptions}>
                        <div className='rounded-lg bg-white shadow' style={styles.loginChoices}>
                            <div className='text-center pt-3 pb-1 border-bottom'>
                                <img src={MoringaLogo} width={50} className='pb-2' alt='Moringa School'/>
                                <h3>Login to Jobs board</h3>
                            </div>
                            <div className='p-4'>
                                {Auth}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
export default AuthPage;