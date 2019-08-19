import {FAIL_GET_PROVIDERS, FIRE_GET_PROVIDERS, PASS_GET_PROVIDERS} from "../actions/types";

const initialState = {
    isLoading: false,
    error: null,
    data: []
};

export default function providersReducer(state=initialState, action) {
    switch (action.type) {
        case FIRE_GET_PROVIDERS:
            return {
                ...state,
                isLoading: true,
                error: null
            };
        case FAIL_GET_PROVIDERS:
            return {
                ...state,
                isLoading: false,
                error: action.error
            };
        case PASS_GET_PROVIDERS:
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