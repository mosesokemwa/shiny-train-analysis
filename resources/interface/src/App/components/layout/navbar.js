import React from "react";
import './navbar.css';

export default class NavBar extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            focused: false
        }
    }

    render() {
        const {focused} = this.state;
        return (
            <nav className={'navbar navbar-light bg-white border-bottom ' + (focused?'nav-hide-sibling':'')}>
                <div className='form-group w-100 mb-1'>
                    <div className='input-group w-100 ml-auto'>
                        <input
                            onFocus={()=>this.setState({focused: true})}
                            onBlur={()=>this.setState({focused: false})}
                            className='form-control w-50 rounded-0 fa'
                            placeholder='&nbsp;&#xF002; Search anything in the Database'
                        />
                    </div>
                </div>
            </nav>
        );
    }
}