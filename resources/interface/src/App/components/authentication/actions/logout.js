import {FIRE_DELETE_AUTH, PASS_DELETE_AUTH, FAIL_DELETE_AUTH} from "./types"
import endpoints from "../../../endpoints";
import xhr from "../../../api";
import check from "./check";

const fire = () => ({
    type: FIRE_DELETE_AUTH,
});

const pass = data => ({
    type: PASS_DELETE_AUTH,
    data: data
});

const fail = message => ({
    type: FAIL_DELETE_AUTH,
    message: message
});

export default function () {
    return dispatch => {
        dispatch(fire());
        xhr.get(endpoints.API_AUTH_LOGOUT)
            .then(({data})=>dispatch(pass(data)))
            .then(({data})=>dispatch(check()))
            .catch(({message})=>dispatch(fail(message)))
    }
}