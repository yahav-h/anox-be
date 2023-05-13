import './RegisrationPage.css';
import React from 'react';
import axios from 'axios';
import LoginComponent from "../Login/LoginPage";


class RegistrationComponent extends React.Component{
    constructor(props) {
        super(props);
        this.state = "state" in props ? props.state : {
            view: "register",
            loaded: false,
            xcsrfToken: null
        };
    }
    setLoadedState(state) {this.state.loaded = state}
    setXcsrfToken(data) {
        this.state.xcsrfToken = data["csrfToken"]
        document.getElementById("reg-form").setAttribute("xcsrf", this.state.xcsrfToken);
    }
    isState() {if (this.state.view === "login") {return 1} else {return 2}}
    render() {
        if (this.isState()===1) {
            return (
                <>
                    <LoginComponent state={this.state} session={null}/>
                </>
            )
        }
        else {
            if (!this.state.loaded) {
                axios.get(
                    window.location.origin + "/flask/v1/register"
                ).then(response => {
                    this.setLoadedState(true)
                    this.setXcsrfToken(response.data)
                })
            }
            return (
                <div className="RegistrationPage">
                      <form id={"reg-form"} className="RegistrationPage-header" xcsrf={""}>
                          <label>
                            <span>
                              Email: <input id={"username"} name={"username"} type={"email"} required={true} placeholder={"alias@company.com"}/>
                            </span>
                          </label>
                          <br/>
                          <label>
                            <span>
                              Password: <input id={"password"} name={"password"} type={"password"} required={true} placeholder={"***************"}/>
                            </span>
                          </label>
                          <br/>
                          <label>
                            <span>
                              Confirm: <input id={"confirm-password"} name={"confirm-password"} type={"password"} required={true} placeholder={"***************"}/>
                            </span>
                          </label>
                          <br/>
                          <label>
                                  <input id={"login-btn"} name={"login-btn"} type={"submit"} value={"SignUp"} onClick={
                                      () => {
                                          const usernameText = document.getElementById("username").value;
                                          const passwordText = document.getElementById("password").value;
                                          axios.post(
                                              window.location.origin + "/flask/v1/register",
                                              {
                                                  payload: btoa(
                                                      JSON.stringify({email: usernameText, password: passwordText})
                                                  )
                                              },
                                          {headers: {"X-CSRF": this.state.xsrfToken}}
                                          )
                                      }
                                  }/>
                              </label>
                          <br/>
                          <label>
                            <a className="RegistrationPage-link" href={"#/login"} onClick={
                            () => {
                              this.setState({view: "login"})
                            }
                          }>back to login</a>
                          </label>
                      </form>
                </div>
            );
        }
    }
}

export default RegistrationComponent;