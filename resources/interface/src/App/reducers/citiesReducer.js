import {FAIL_GET_CITIES, FIRE_GET_CITIES, PASS_GET_CITIES} from "../actions/types";

const initialState = {
    isLoading: false,
    error: null,
    data: []
};

export default function citiesReducer(state=initialState, action) {
    switch (action.type) {
        case FIRE_GET_CITIES:
            return {
                ...state,
                isLoading: true,
                error: null
            };
        case FAIL_GET_CITIES:
            return {
                ...state,
                isLoading: false,
                error: action.error
            };
        case PASS_GET_CITIES:
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