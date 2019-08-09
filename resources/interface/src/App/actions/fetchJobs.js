import {FAIL_GET_JOBS, FIRE_GET_JOBS, PASS_GET_JOBS} from "../actions/types"
import endpoints from "../endpoints";
import api from "../api";

function fireGet() {
    return {
        type: FIRE_GET_JOBS
    }
}

function failGet(error) {
    return {
        type: FAIL_GET_JOBS,
        error: error
    }
}

function passGet(data) {
    return {
        type: PASS_GET_JOBS,
        data: data
    }
}

export default function fetchJobs(filters={}, sorting={}){
    return dispatch => {
        dispatch(fireGet());
        console.log(filters, sorting);
        api.get(endpoints.JOBS, {
            params: {
                ...filters,
                ...sorting
            }
        })
            .then(data => data.data)
            .then(data => dispatch(passGet(data)))
            .catch(error => dispatch(failGet(error.message)))
    }
}