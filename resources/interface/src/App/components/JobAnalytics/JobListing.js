import React from "react"
import moment from "moment";
import "./job-listing.css"

class Listing extends React.PureComponent{
    render() {
        const {jobs} = this.props;
        return (
            <tbody>
            {
                jobs.map(
                    job => (
                        <tr key={Math.random()}>
                            <td>{job['id']}</td>
                            <td className='position-relative'>
                                <span className='mr-2'>{job['title']}</span>
                                {job['skills']!==null?<i
                                    className='fa fa-info-circle position-absolute text-muted hover-dark mt-1'
                                    style={{cursor: 'pointer'}}
                                    title={'\u2022 ' + (job['skills']||[]).join('\n\u2022 ')}
                                />:null}
                            </td>
                            <td>{job['organization']}</td>
                            <td>{job['city']?`${job['city']}, ${job['country']}`:''}</td>
                            <td>{job['type']}</td>
                            <td>{moment(job['posted']).format('MMM Do YYYY')}</td>
                            <td>{job['deadline']?moment(job['deadline']).format('MMM Do YYYY'):'Unknown'}</td>
                            <td>
                                <a href={job.url} target='_blank' rel='noreferrer noopener'>
                                    <button className='btn btn-primary'>
                                        View
                                    </button>
                                </a>
                            </td>
                        </tr>
                    )
                )
            }
            </tbody>
        )
    }
}

export default class JobListing extends React.PureComponent{
    render() {
        const {jobs, updateSort, sorting} = this.props;
        const sortable_fields = ['id', 'title', 'organization', 'cities', 'type', 'posted', 'deadline'];
        const makeSort = (field)=>{
            if(sorting.sortBy!==field){
                return sortable_fields.includes(field);
            } else {
                return sorting.order==='asc'?'desc':'asc'
            }
        };
        const heading = [
            ['id', '#', makeSort('id')],
            ['title', 'Title', makeSort('title')],
            ['organization', 'Company', makeSort('organization')],
            ['cities', 'City', makeSort('cities')],
            ['type', 'Type', makeSort('type')],
            ['posted', 'Posted', makeSort('posted')],
            ['deadline', 'Deadline', makeSort('deadline')],
            ['url', 'Link', makeSort('url')]
        ];
        return (
            <div className='table-responsive'>
                <table className='table table-hover table-striped'>
                    <thead>
                    <tr style={{whiteSpace: 'nowrap'}}>
                        {
                            heading.map(
                                ([field, title, order])=>(
                                    <th key={`title--${field}`} style={{cursor: 'pointer'}}>
                                        {!order?title:
                                            <span onClick={()=>updateSort(field, (order===true?'asc':(order?order:'asc')))}>
                                                {title}
                                                {order===true?
                                                    <span className='fa ml-1 text-muted' style={{opacity: .4}}>
                                                        <span className='fa-caret-down'/>
                                                        <span className='fa-caret-up ml-1'/>
                                                    </span>:
                                                    <span className={'fa ml-1 fa-caret-' + (order==='desc'?'down':'up')}/>
                                                }
                                            </span>
                                        }
                                    </th>
                                ))
                        }
                    </tr>
                    </thead>
                    <Listing jobs={jobs}/>
                </table>
            </div>
        )
    }
}
