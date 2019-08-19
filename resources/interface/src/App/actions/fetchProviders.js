import {FAIL_GET_PROVIDERS, FIRE_GET_PROVIDERS, PASS_GET_PROVIDERS} from "../actions/types"
import endpoints from "../endpoints";
import api from "../api";

function fireGet() {
    return {
        type: FIRE_GET_PROVIDERS
    }
}

function failGet(error) {
    return {
        type: FAIL_GET_PROVIDERS,
        error: error
    }
}

function passGet(data) {
    return {
        type: PASS_GET_PROVIDERS,
        data: data
    }
}

export default function fetchProviders(){
    return dispatch => {
        dispatch(fireGet());
        api.get(endpoints.PROVIDERS)
            .then(data => data.data)
            .then(data => dispatch(passGet(data)))
            .catch(error => dispatch(failGet(error.message)))
    }
}