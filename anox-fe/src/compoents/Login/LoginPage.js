import './LoginPage.css';
import React from 'react';
import axios from 'axios';
import ResetPasswordComponent from "../Reset/ResetPasswordPage";
import RegistrationComponent from "../Register/RegistrationPage";
import DashboardPage from "../Dashboard/DashboardPage";


class LoginComponent extends React.Component {

    constructor(props) {
        super(props);
        this.state = "state" in props ? props.state : {view: "login"}
        this.session = "session" in props ? props.session : sessionStorage.getItem("__anoxsys_session__")
    }

    isState = () => {
        if (this.state.view === "dashboard") {return 1}
        else if (this.state.view === "reset") {return 2}
        else if (this.state.view === "register") {return 3}
        else {return 4}
    }

    userLoginHandler() {
        const usernameText = document.getElementById("username").value;
        const passwordText = document.getElementById("password").value;
        if (!usernameText || !passwordText) {
            alert("username / password are required!");
        } else {
            axios.post(
            window.location.origin + "/flask/v1/login",
            {
                payload: btoa(JSON.stringify({email: usernameText, password: passwordText}))
            }
        ).then((response) => {
            const authToken = response.headers.get("Authorization")
            sessionStorage.setItem("__anoxsys_session__", authToken)
        }).then(()=>{
            this.setState({view: "dashboard"});
            window.location.href = "#/dashboard"
        })
        }
    }

    render() {
        if (this.isState()===1 || this.session) {
            return (
                <>
                    <DashboardPage session={this.session}/>
                </>
            );
        }
        else if (this.isState()===2) {
            return (
                <>
                    <ResetPasswordComponent />
                </>
            )
        }
        else if (this.isState()===3) {
            return (
                <>
                    <RegistrationComponent />
                </>
            )
        } else if (this.isState()===4){
            return (
                <div className="LoginPage">
                  <header className="LoginPage-header">
                      <label>
                        <span>
                          <input id={"username"} name={"username"} type={"email"}
                                 required={true} placeholder={"alias@company.com"}
                          />
                        </span>
                      </label>
                      <br/>
                      <label>
                        <span>
                          <input id={"password"} name={"password"} type={"password"}
                                 required={true} placeholder={"************"}
                          />
                        </span>
                      </label>
                      <br/>
                      <label>
                          <input id={"login-btn"} name={"login-btn"} type={"submit"}
                                 value={"Login"} onClick={() => {this.userLoginHandler();}}
                          />
                      </label>
                      <br/>
                      <ul>
                          <a className="LoginPage-link" href={"#/reset-password"}
                             onClick={() => {this.setState({view: "reset"})
                             }
                          }>
                          reset password
                      </a>
                      {"   |   "}
                      <a className="LoginPage-link" href={"#/register"} onClick={
                          () => {this.setState({view: "register"})}
                      }>register now</a>
                      </ul>
                  </header>
                </div>
            );
        }
    }
}

export default LoginComponent;