import * as React from "react";
import "./styles/drop-down-checkbox.css"

export default class DropDownCheckbox extends React.PureComponent{
    constructor(props) {
        super(props);
        this.state = {
            selected: []
        }
    }

    callBack(){
        const {onChange} = this.props;
        if (onChange){
            onChange(this.state.selected)
        }
    }

    toggleOption(option) {
        const {selected} = this.state;
        if (selected.includes(option)){
            this.setState({selected: selected.filter(s => s!==option)}, this.callBack)
        } else {
            this.setState({selected: [...selected, option]}, this.callBack)
        }
    }

    render() {
        const {options, title} = this.props;
        const {selected} = this.state;
        return (
            <div className='drop-down-checkbox position-relative'>
                <div className='drop-down-checkbox-title'>
                    <button className='btn btn-secondary dropdown-toggle'>
                        {title}
                    </button>
                </div>
                <div className='drop-down-checkbox-listing border mt-2 rounded p-1' tabIndex={0}>
                    {options.map(
                        (option, idx) => (
                            <div className='drop-down-checkbox-control custom-control custom-checkbox mx-3' key={idx}>
                                <input type='checkbox' className='custom-control-input' id={`job-type-${idx}`} checked={selected.includes(option)} onChange={_ => this.toggleOption(option)}/>
                                <label className='custom-control-label' htmlFor={`job-type-${idx}`}>
                                    <span>{option}</span>
                                </label>
                            </div>
                        )
                    )}
                    <div className='mx-n1 mb-n1 mt-2 border-top px-2 drop-down-checkbox-listing-clear' onClick={()=>this.setState({selected: []}, this.callBack)}>
                        <i className='fa fa-times'/> Clear
                    </div>
                </div>
            </div>
        );
    }
}