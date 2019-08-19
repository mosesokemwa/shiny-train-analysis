import {FAIL_GET_CITIES, FIRE_GET_CITIES, PASS_GET_CITIES} from "../actions/types"
import endpoints from "../endpoints";
import api from "../api";

function fireGet() {
    return {
        type: FIRE_GET_CITIES
    }
}

function failGet(error) {
    return {
        type: FAIL_GET_CITIES,
        error: error
    }
}

function passGet(data) {
    return {
        type: PASS_GET_CITIES,
        data: data
    }
}

export default function fetchCities(){
    return dispatch => {
        dispatch(fireGet());
        api.get(endpoints.CITIES)
            .then(data => data.data)
            .then(data => dispatch(passGet(data.locations)))
            .catch(error => dispatch(failGet(error.message)))
    }
}