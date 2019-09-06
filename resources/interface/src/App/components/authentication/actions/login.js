import {FIRE_POST_AUTH, PASS_POST_AUTH, FAIL_POST_AUTH} from "./types"
import endpoints from "../../../endpoints";
import xhr from "../../../api";
import check from "./check";

const firePostAuth = provider => ({
    type: FIRE_POST_AUTH,
    provider: provider
});

const passPostAuth = () => ({
    type: PASS_POST_AUTH
});

const failPostAuth = message => ({
    type: FAIL_POST_AUTH,
    message: message
});

export default function (type, data) {
    return dispatch => {
        dispatch(firePostAuth(type));
        switch (type) {
            case 'google':
                xhr.get(endpoints.API_AUTH_GOOGLE, {params: {code: data}})
                    .then(({data})=>{
                        localStorage.setItem('user_token', data.token);
                        dispatch(check());
                        dispatch(passPostAuth(data))
                    })
                    .catch(({message})=>dispatch(failPostAuth(message)));
                break;
            case 'canvas':
                xhr.get(endpoints.API_AUTH_CANVAS, {params: {code: data}})
                    .then(({data})=>{
                        localStorage.setItem('user_token', data.token);
                        dispatch(check());
                        dispatch(passPostAuth(data))
                    })
                    .catch(({message})=>dispatch(failPostAuth(message)));
                break;
            default:
                dispatch(failPostAuth('Unknown Auth method'))
        }
    }
}