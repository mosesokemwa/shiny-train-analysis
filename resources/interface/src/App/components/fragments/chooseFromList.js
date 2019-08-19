import React from "react";
import "./styles/chooseFromList.css";

export default class ChooseFromList extends React.Component{
    static defaultProps = {
        onChoose: _=>_
    };
    constructor(props) {
        super(props);
        this.input = React.createRef();
        this.state = {
            value: '',
            chosen: []
        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevState.chosen !== this.state.chosen){
            this.props.onChoose(this.state.chosen)
        }
    }

    toggleItem(item) {
        this.input.focus();
        const {chosen} = this.state;
        if (chosen.includes(item)){
            this.setState({value: '', chosen: chosen.filter(c=>c!==item)})
        } else {
            this.setState({value: '', chosen: [...chosen, item]})
        }
    }

    render() {
        const {chosen, value} = this.state;
        const {choices} = this.props;
        let available = [];
        available = choices.filter(c=>c.toLowerCase().startsWith(value.toLowerCase()));
        const chooseOne = () => {
            if (available.length === 1){
                this.setState({value: '', chosen: [...chosen, available[0]]})
            }
        };
        return (
            <div className='position-relative'>
                <div className='choice-input form-control d-flex m-0 flex-wrap' onClick={()=>this.input.focus()}>
                    {chosen.map(
                        (choice, idx) => (
                            <span className='border rounded px-1 mb-1 mr-1 bg-light' key={idx}>
                                <span
                                    className='fa fa-times pointer'
                                    onClick={()=>this.setState({chosen: chosen.filter(c=>c!==choice)})}
                                >
                                    &nbsp;
                                </span>
                                {choice}
                            </span>
                        )
                    )}
                    <input
                        className='live-input p-0'
                        autoComplete='off'
                        size='1'
                        value={value}
                        onKeyDown={e=>e.keyCode===13?chooseOne():null}
                        onChange={({currentTarget})=>this.setState({value: currentTarget.value})}
                        ref={(input)=>this.input=input}
                    />
                    <div className='input-suggestions bg-white rounded'>
                        {available.map(
                            (item, index) => (
                                <div
                                    key={index} className='pointer hover-bg border border-top-0'
                                    onClick={()=>this.toggleItem(item)}
                                >
                                    <div className='p-1'>{item} {chosen.includes(item)?<span className='fa fa-pull-right fa-dot-circle-o text-black-50'/>:null}</div>
                                </div>
                            )
                        )}
                    </div>
                </div>
            </div>
        )
    }
}