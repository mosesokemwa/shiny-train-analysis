import {combineReducers} from "redux";
import jobsReducer from "./jobsReducer";
import tagsReducer from "./tagsReducer";
import citiesReducer from "./citiesReducer";
import providersReducer from "./providersReducer";
import syncReducer from "./syncReducer";

export default combineReducers({
    jobs: jobsReducer,
    tags: tagsReducer,
    cities: citiesReducer,
    sync: syncReducer,
    providers: providersReducer
})