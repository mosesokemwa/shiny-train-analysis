import React from "react";
import {connect} from "react-redux";
import fetchJobs from "../../actions/fetchJobs";
import JobListing from "./JobListing";
import fetchTags from "../../actions/fetchTags";
import ChooseFromList from "../fragments/chooseFromList";
import DropDownCheckbox from "../fragments/DropDownCheckbox";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from "moment";
import fetchCities from "../../actions/fetchCities";

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
                deadline: moment().format("YYYY-MM-DD"),
                deadlineBlank: true,
                page_size: 25,
                page: 1
            },
            sorting: {
                sortBy: 'id',
                order: 'asc'
            }
        }
    }

    componentDidMount() {
        const {jobId} = this.props.match.params;
        const doFetch = () => this.props.fetchJobs(this.state.filters, this.state.sorting);
        if (jobId !== undefined){
            this.setState({...this.state,filters: {...this.state.filters, provider_id: jobId}}, doFetch);
        } else {
            doFetch()
        }
        this.props.fetchTags();
        this.props.fetchCities();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        const {jobId} = this.props.match.params;
        const prevJobId = prevProps.match.params['jobId'];
        const currentJobId = this.state.filters.provider_id;
        if (jobId !== prevJobId && jobId !== currentJobId){
            let newFilters;
            if (jobId !== undefined){
                newFilters = {...this.state.filters, provider_id: jobId, page: 1};
            } else {
                newFilters = {...this.state.filters, page: 1};
                delete newFilters['provider_id'];
            }
            this.setState({filters: newFilters});
        }
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

    updateExperience(experience) {
        const filters = {...this.state.filters};
        if (experience.length === 0){
            delete filters['experience'];
            this.setState({filters})
        } else {
            this.setState({filters: {...filters, experience}});
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

    updateDateValue(date, name) {
        this.setState({filters: {...this.state.filters, [name]: moment(date).format("YYYY-MM-DD")}})
    }

    updateCities(cities) {
        this.setState({filters: {...this.state.filters, cities : cities}})

    }

    toggleDeadlineBlank() {
        const {deadlineBlank} = this.state.filters;
        const f = {...this.state.filters};
        if (deadlineBlank){
            delete f['deadlineBlank'];
            this.setState({filters: f})
        } else {
            this.setState({filters: {...f, deadlineBlank: true}})
        }
    }

    renderFilters(){
        const {jobTypes} = this.state;
        const {tags, cities} = this.props;
        const {types, deadline, posted, experience, deadlineBlank} = this.state.filters;
        const experienceOptions = ['Entry Level', 'Junior', 'Mid Level', 'Senior', 'Other (Not Specified)'];
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
                        <label>City</label>
                        <ChooseFromList
                            withInput
                            choices={cities}
                            onChoose={cities=>this.updateCities(cities)}
                        />
                    </div>
                    <div className='form-group col'>
                        <label>Technologies</label>
                        <ChooseFromList choices={tags} onChoose={(technologies)=>this.updateTechnologies(technologies)}/>
                    </div>
                    <div className='form-group col d-none'>
                        <label>&nbsp;</label>
                        <div>
                            <DropDownCheckbox
                                title={'Professional Experience' + (experience?` ${experience.length}/${experienceOptions.length}`:'')}
                                onChange={experience=>this.updateExperience(experience)}
                                options={experienceOptions}
                            />
                        </div>
                    </div>
                    <div className='form-group flex-wrap col d-none'>
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
                        <DatePicker
                            className="form-control"
                            selected={posted?(moment(posted, "YYYY-MM-DD")).toDate():null}
                            onChange={date => this.updateDateValue(date, 'posted')}
                            dateFormat="MMMM d, yyyy"
                        />
                        <small className='form-text text-muted'>All jobs posted after this date.</small>
                    </div>
                    <div className='form-group col-lg-3 col-md-3 col-sm-4 col-6'>
                        <label>Deadline</label>
                        <DatePicker
                            className="form-control"
                            selected={(moment(deadline, "YYYY-MM-DD")).toDate()}
                            onChange={date => this.updateDateValue(date, 'deadline')}
                            dateFormat="MMMM d, yyyy"
                        />
                        <small className='form-text text-muted'>All jobs valid after this deadline.</small>
                        <div className="custom-control custom-checkbox small text-muted">
                            <input type="checkbox" checked={!!deadlineBlank} className="custom-control-input" id="unknownDeadline" onChange={()=>this.toggleDeadlineBlank()}/>
                            <label className="custom-control-label pt-1" htmlFor="unknownDeadline">Unknown Deadline</label>
                        </div>
                    </div>
                    <div className='form-row'>
                        <div className='form-group'>
                            <label>Page limit</label>
                            <select onChange={e => this.updateValue(e)} name='page_size' className='custom-select'>
                                <option key={25}>25</option>
                                <option key={50}>50</option>
                                <option key={75}>75</option>
                                <option key={100}>100</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    toPage(page) {
        if (page !== this.state.filters.page) {
            return this.setState({filters: {...this.state.filters, page}});
        }
    }

    renderPagination(){
        const {count, page, jobs} = this.props;
        const size = this.state.filters.page_size || 100;
        const last = Math.ceil(count / size);
        const pages = [1, '...', page-1, page, page+1, '...', last];
        if (page === 1){
            pages.splice(0, 3)
        }
        if (page === 2){
            pages.splice(0, 2)
        }
        if (page === (last-1)){
            pages.splice(-2, 2)
        }
        if (page === last){
            pages.splice(-3, 3)
        }
        return (
            <div className='p-2 d-flex justify-content-between'>
                <ul className='pagination'>
                    {page === 1?null:(
                        <>
                            <li className='page-item'>
                                <div className='page-link pointer' onClick={()=>this.toPage(page-1)}>«</div>
                            </li>
                        </>
                    )}
                    {pages.map((pg, c) =>
                        <li key={c} className={'page-item ' + (pg===page?'active':'')}>
                            <div className='page-link pointer' onClick={()=>(pg!=='...'?this.toPage(pg):null)}>{pg}</div>
                        </li>
                    )}
                    {page === last?null:(
                        <li className='page-item'>
                            <div className='page-link pointer' onClick={()=>this.toPage(page+1)}>»</div>
                        </li>
                    )}
                </ul>
                <div className='mr-3'>
                    Showing <b>{(page-1)*size + 1} to {(page-1)*size + jobs.length}</b> of {count}
                </div>
            </div>
        )
    }

    render() {
        const {jobs, isLoading, providers, match} = this.props;
        const {sorting} = this.state;
        const {jobId} = match.params;
        const provider = providers.find(p => p.id === parseInt(jobId));
        const {page} = this.props;
        const size = this.state.filters.page_size || 100;
        const offset = (page - 1) * size;
        return (
            <div className='m-3 shadow'>
                <h4 className='text-center p-2 m-0'>{provider?provider.name:'All '} Jobs</h4>
                <div style={{borderTop: '1px solid rgba(221, 221, 221, 0.22)'}}>
                    {this.renderFilters()}
                </div>
                {this.renderPagination()}
                <div style={{opacity: isLoading?0.5:1}}>
                    <JobListing
                        offset={offset}
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
        count: state.jobs.count,
        page: state.jobs.page,
        tags: state.tags.data,
        cities: state.cities.data,
        providers: state.providers.data,
        isLoading: state.jobs.isLoading
    }
}
export default connect(mapStateTopProps, {fetchJobs, fetchTags, fetchCities})(JobAnalytics)
