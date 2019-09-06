import * as types from "./actions/types"

const initialState = {
    isLoading: false,
    isAuthenticated: false,
    user: null,
    error: null
};

export function authentication(state=initialState, action){
    switch (action.type) {
        case types.FIRE_POST_AUTH:
            return {
                isLoading: true,
                isAuthenticated: false,
                user: null,
                error: null
            };
        case types.FIRE_CHECK_AUTH:
        case types.FIRE_DELETE_AUTH:
            return {
                ...state,
                isLoading: true
            };
        case types.PASS_POST_AUTH:
        case types.PASS_DELETE_AUTH:
            return state;
        case types.PASS_CHECK_AUTH:
            return {
                isAuthenticated: action.data.isAuthenticated,
                user: action.data.user,
                isLoading: false
            };
        case types.FAIL_POST_AUTH:
            return {
                isLoading: false,
                error: action.message
            };
        case types.FAIL_CHECK_AUTH:
            return {
                isLoading: false,
                error: action.message
            };
        default:
            return state;
    }
}