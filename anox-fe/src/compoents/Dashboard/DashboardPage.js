import './DashboardPage.css';
import React, { useEffect, useState } from 'react';
import { FaCog } from 'react-icons/fa';


class DashboardComponent extends React.Component{
    constructor(props) {
        super(props);
        this.state = "state" in props ? props.state : {
            view:"dashboard",
            loaded: false
        };
        this.session = "session" in props ? props.session : sessionStorage.getItem("__anoxsys_session__");
        console.log(this)
    }

    topRtMenuHandler () {

    }

    render() {
        return (
            <div className="DashboardPage">
                <div className="DashboardPage-leftSideFacet">
                    <div>
                        <div className="DashboardPage-imageContainer">
                            <img src="#"/>
                        </div>
                        <div className="">

                        </div>
                    </div>
                </div>
                <div className="DashboardPage-topRightSideMenu">
                    <div className="top-rt-menu-container">
                        <ul className="top-rt-menu-wrapper">
                            <li className="top-rt-menu-btn-wrapper">
                                <FaCog  onClick={()=>{
                                    this.topRtMenuHandler()
                                }}/>
                            </li>
                            <li className="current-user-in-session">
                                <div>yahavh@avanan.com</div>
                            </li>
                        </ul>
                    </div>
                </div>
                <header className="DashboardPage-header"></header>
            </div>
        );
    }
}

export default DashboardComponent;