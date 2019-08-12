import React from "react";
import {connect} from "react-redux";
import fetchJobs from "../../actions/fetchJobs";
import JobListing from "./JobListing";
import moment from "moment";
import fetchTags from "../../actions/fetchTags";
import ChooseFromList from "../fragments/chooseFromList";

class JobAnalytics extends React.Component{
    constructor(props) {
        super(props);
        this.timeout = null;
        this.state = {
            jobTypes: [
                'Full Time',
                'Part Time',
                'Contract',
                'Internship',
                'Attachment'
            ],
            filters: {
                deadline: (new moment()).format("YYYY-MM-DD")
            },
            sorting: {
                sortBy: 'id',
                order: 'asc'
            }
        }
    }

    componentDidMount() {
        this.props.fetchJobs(this.state.filters, this.state.sorting);
        this.props.fetchTags();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        clearTimeout(this.timeout);
        if (this.state.filters !== prevState.filters || this.state.sorting !== prevState.sorting){
            this.timeout = setTimeout(()=>this.props.fetchJobs(this.state.filters, this.state.sorting), 500)
        }
    }

    updateValue(event) {
        this.setState({filters: {...this.state.filters, [event.target.name]: event.target.value}})
    }

    updateTechnologies(technologies){
        const filters = {...this.state.filters};
        if (technologies.length === 0){
            delete filters['tags'];
            this.setState({filters})
        } else {
            this.setState({filters: {...filters, tags: technologies}});
        }
    }

    toggleJobType(jobType) {
        const filters = this.state.filters;
        let types = [...(filters.types||[])];
        if (types.includes(jobType)){
            types.splice(types.indexOf(jobType), 1)
        } else {
            types.push(jobType)
        }
        if (types.length === 0 ){
            const filters = {...this.state.filters};
            delete filters['types'];
            this.setState({filters});
        } else {
            this.setState({filters: {...filters, types}});
        }
    }

    renderFilters(){
        const {jobTypes} = this.state;
        const {tags} = this.props;
        const {types, deadline, posted} = this.state.filters;
        return (
            <div className='p-4'>
                <div className='form-row'>
                    <div className='form-group col-6'>
                        <label>Job Title</label>
                        <input className='form-control' name='title' placeholder='Job Title' onInput={event => this.updateValue(event)} />
                    </div>
                    <div className='form-group col-6'>
                        <label>Company Name</label>
                        <input className='form-control' name='organization' placeholder='Company' onInput={event => this.updateValue(event)} />
                    </div>
                    <div className='form-group col-4'>
                        <label>Location</label>
                        <input className='form-control' name='location' placeholder='Location' onInput={event => this.updateValue(event)} />
                    </div>
                    <div className='form-group col'>
                        <label>Technologies</label>
                        <ChooseFromList choices={tags} onChoose={(technologies)=>this.updateTechnologies(technologies)}/>
                    </div>
                    <div className='form-group flex-wrap col'>
                        <div>
                            <label>Job Type</label>
                        </div>
                        <div className='d-flex'>
                            {jobTypes.map(
                                jobType => {
                                    const unique = (Math.random() + '').replace('.', '');
                                    return (
                                        <div className='custom-control custom-checkbox mx-3' key={unique}>
                                            <input type='checkbox' className='custom-control-input' id={`job-type-${unique}`} checked={types&&types.includes(jobType)} onChange={_ => this.toggleJobType(jobType)}/>
                                            <label className='custom-control-label' htmlFor={`job-type-${unique}`}>
                                                <span>{jobType}</span>
                                            </label>
                                        </div>
                                    )
                                }
                            )}
                        </div>
                    </div>
                </div>
                <div className='form-row'>
                    <div className='form-group col-lg-3 col-md-3 col-sm-4 col-6'>
                        <label>Posted after</label>
                        <input type='date' className='form-control' name='posted' value={posted} onInput={event =>this.updateValue(event)}/>
                        <small className='form-text text-muted'>All jobs posted after this date.</small>
                    </div>
                    <div className='form-group col-lg-3 col-md-3 col-sm-4 col-6'>
                        <label>Deadline</label>
                        <input type='date' className='form-control' name='deadline' value={deadline} onChange={event =>this.updateValue(event)}/>
                        <small className='form-text text-muted'>All jobs before this deadline.</small>
                    </div>
                </div>
            </div>
        )
    }

    render() {
        const {jobs, isLoading} = this.props;
        const {sorting} = this.state;
        return (
            <div className='m-3 shadow-sm'>
                {this.renderFilters()}
                <div style={{opacity: isLoading?0.5:1}}>
                    <JobListing
                        jobs={jobs}
                        updateSort={(sortBy, order)=>this.setState({sorting: {sortBy, order}})}
                        sorting={sorting}
                    />
                </div>
            </div>
        );
    }
}

function mapStateTopProps(state){
    return {
        jobs: state.jobs.data,
        tags: state.tags.data,
        isLoading: state.jobs.isLoading
    }
}
export default connect(mapStateTopProps, {fetchJobs, fetchTags})(JobAnalytics)
