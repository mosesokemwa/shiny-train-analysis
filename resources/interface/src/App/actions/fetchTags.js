import {FAIL_GET_TAGS, FIRE_GET_TAGS, PASS_GET_TAGS} from "../actions/types"
import endpoints from "../endpoints";
import api from "../api";

function fireGet() {
    return {
        type: FIRE_GET_TAGS
    }
}

function failGet(error) {
    return {
        type: FAIL_GET_TAGS,
        error: error
    }
}

function passGet(data) {
    return {
        type: PASS_GET_TAGS,
        data: data
    }
}

export default function fetchTags(){
    return dispatch => {
        dispatch(fireGet());
        api.get(endpoints.TAGS)
            .then(data => data.data)
            .then(data => dispatch(passGet(data)))
            .catch(error => dispatch(failGet(error.message)))
    }
}