import {FAIL_GET_JOBS, FIRE_GET_JOBS, PASS_GET_JOBS} from "../actions/types";

const initialState = {
    isLoading: false,
    error: null,
    data: []
};

export default function jobsReducer(state=initialState, action) {
    switch (action.type) {
        case FIRE_GET_JOBS:
            return {
                ...state,
                isLoading: true,
                error: null
            };
        case FAIL_GET_JOBS:
            return {
                ...state,
                isLoading: false,
                error: action.error
            };
        case PASS_GET_JOBS:
            return {
                ...state,
                error: null,
                isLoading: false,
                data: action.data
            };
        default:
            return state;
    }
}