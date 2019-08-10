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

    render() {
        const {chosen, value} = this.state;
        const {choices} = this.props;
        let available = [];
        if (value!==''){
            available = choices.filter(c=>(!chosen.includes(c))&&c.toLowerCase().startsWith(value.toLowerCase()));
        }
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
                            <span className='border rounded px-1 m-1 bg-light' key={idx}>
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
                    {/*{value?*/}
                    <div className='input-suggestions bg-white rounded'>
                        <table className='table table-hover border'>
                            <tbody>
                            {available.map(
                                (item, index) => (
                                    <tr
                                        key={index} className='pointer'
                                        onClick={()=>this.setState({value: '', chosen: [...chosen, item]})}
                                    >
                                        <td className='p-1'>{item}</td>
                                    </tr>
                                )
                            )}
                            </tbody>
                        </table>
                    </div>
                    {/*:null}*/}
                </div>
            </div>
        )
    }
}