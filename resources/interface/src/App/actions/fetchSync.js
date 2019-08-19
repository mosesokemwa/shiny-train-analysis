import {FAIL_GET_SYNC, FIRE_GET_SYNC, PASS_GET_SYNC} from "../actions/types"
import endpoints from "../endpoints";
import api from "../api";

function fireGet() {
    return {
        type: FIRE_GET_SYNC
    }
}

function failGet(error) {
    return {
        type: FAIL_GET_SYNC,
        error: error
    }
}

function passGet(data) {
    return {
        type: PASS_GET_SYNC,
        data: data
    }
}

export default function fetchSync(){
    return dispatch => {
        dispatch(fireGet());
        api.get(endpoints.SYNC)
            .then(data => data.data)
            .then(data => dispatch(passGet(data)))
            .catch(error => dispatch(failGet(error.message)))
    }
}