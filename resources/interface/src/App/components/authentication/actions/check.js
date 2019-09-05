import {FIRE_CHECK_AUTH, PASS_CHECK_AUTH, FAIL_CHECK_AUTH} from "./types"
import endpoints from "../../../endpoints";
import xhr from "../../../api";

const fireCheckAuth = () => ({
    type: FIRE_CHECK_AUTH,
});

const passCheckAuth = data => ({
    type: PASS_CHECK_AUTH,
    data: data
});

const failCheckAuth = message => ({
    type: FAIL_CHECK_AUTH,
    message: message
});

export default function () {
    return dispatch => {
        dispatch(fireCheckAuth());
        xhr.get(endpoints.API_AUTH_CHECK)
            .then(({data})=>dispatch(passCheckAuth({isAuthenticated: true, user: data})))
            .catch((error)=>{
                if (error.response && error.response.status === 403){
                    dispatch(passCheckAuth({isAuthenticated: false, user: null}));
                } else {
                    dispatch(failCheckAuth(error.message))
                }
            })
    }
}