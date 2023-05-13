import './ResetPasswordPage.css';
import React from 'react';
import axios from 'axios';
import LoginPage from "../Login/LoginPage";


class ResetPasswordComponent extends React.Component{
    constructor(props) {
        super(props);
        this.state = "state" in props ? props.state : {
            sentReset: false, view: "reset",
            loaded: false,
            xcsrfToken: null
        };
    }
    setLoadedState(state) {this.state.loaded = state}
    setXcsrfToken(data) {
        this.state.xcsrfToken = data["csrfToken"]
        document.getElementById("reset-form").setAttribute("xcsrf", this.state.xcsrfToken);
    }
    isState () {
        if (this.state.view === "login") {return 1}
        else {return 2}
    }
    render() {
        if (!this.state.loaded) {
            axios.get(
                    window.location.origin + '/flask/v1/reset-password'
                ).then(response => {
                    this.setLoadedState(true)
                    this.setXcsrfToken(response.data)
                })
        }
        if (this.isState()===1) {
            return (
                <>
                    <LoginPage />
                </>
            )
        }
        return (
            <div className="ResetPasswordPage">
              <form id={"reset-form"} className="ResetPasswordPage-header" csrf={""}>
                  <p>enter your email account to reset your password</p>
                  <label>
                    <span>
                      <input id={"username"} name={"username"} type={"email"} required={true} placeholder={"alias@company.com"}/>
                    </span>
                  </label>
                  <br/>
                  <label>
                      <input
                          id={"reset-btn"} name={"reset-btn"}
                          type={"submit"} value={"Reset"}
                          onClick={
                              () => {
                                  const email = document.getElementById("username").value;
                                  const payload = btoa(JSON.stringify({email: email, timestamp: Date.now()}));
                                  axios.post(
                                      window.location.origin + '/flask/v1/reset-password',
                                      {payload: payload},
                                      {
                                          headers: {"X-CSRF": this.state.xcsrfToken}
                                      }
                                  ).then(response => {
                                    console.log("SUCCESS", response)
                                  }).catch(error => {
                                    console.log(error)
                                  })
                              }
                          }
                      />
                  </label>
                  <br/>
                  <a className="ResetPage-link" href={"#/login"} onClick={
                      () => {
                          this.setState({view: "login"})
                      }
                  }>
                      back to login
                  </a>
              </form>
            </div>
          );
    }
}

export default ResetPasswordComponent;