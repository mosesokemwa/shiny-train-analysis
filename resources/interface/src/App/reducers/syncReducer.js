import {FAIL_GET_SYNC, FIRE_GET_SYNC, PASS_GET_SYNC} from "../actions/types";

const initialState = {
    isLoading: false,
    error: null,
    data: {
        created_at: 0
    }
};

export default function syncReducer(state=initialState, action) {
    switch (action.type) {
        case FIRE_GET_SYNC:
            return {
                ...state,
                isLoading: true,
                error: null
            };
        case FAIL_GET_SYNC:
            return {
                ...state,
                isLoading: false,
                error: action.error
            };
        case PASS_GET_SYNC:
            return {
                ...state,
                error: null,
                isLoading: false,
                data: action.data[0]
            };
        default:
            return state;
    }
}