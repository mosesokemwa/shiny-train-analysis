import {FAIL_GET_TAGS, FIRE_GET_TAGS, PASS_GET_TAGS} from "../actions/types";

const initialState = {
    isLoading: false,
    error: null,
    data: []
};

export default function jobsReducer(state=initialState, action) {
    switch (action.type) {
        case FIRE_GET_TAGS:
            return {
                ...state,
                isLoading: true,
                error: null
            };
        case FAIL_GET_TAGS:
            return {
                ...state,
                isLoading: false,
                error: action.error
            };
        case PASS_GET_TAGS:
            return {
                ...state,
                error: null,
                isLoading: false,
                data: action.data['tags']
            };
        default:
            return state;
    }
}