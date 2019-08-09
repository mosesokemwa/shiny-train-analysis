import React from "react";
import NavBar from "./navbar";
import SideBar from "./sidebar";

export default class Layout extends React.Component{
    render() {
        return (
            <div>
                <div className='row m-0'>
                    <div className='col-lg-2 col-1'>
                        <SideBar/>
                    </div>
                    <div className='col-lg-10 col-11 p-0'>
                        <NavBar/>
                        <div>
                            {this.props.children}
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}