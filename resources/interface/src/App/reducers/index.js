import {combineReducers} from "redux";
import jobsReducer from "./jobsReducer";
import tagsReducer from "./tagsReducer";

export default combineReducers({
    jobs: jobsReducer,
    tags: tagsReducer
})