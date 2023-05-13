import React from 'react';
import LoginComponent from './compoents/Login/LoginPage';


class App extends React.Component{

  render() {
      return (
          <>
            <LoginComponent/>
          </>
      );
    }
}

export default App;





// import logo from './logo.svg';
// import './App.css';
// import React, { useEffect, useState } from 'react';
// import { ReactSession } from 'react-client-session';
// import {Routes, Route, Router} from 'react-router-dom';
// import axios from 'axios';
// import LoginComponent from "./Login/LoginPage";
// import RegistrationComponent from './Register/RegistrationPage';
// import ResetPasswordComponent from './Reset/ResetPasswordPage';
//
// function toJWT(sessionObject) { return btoa(JSON.stringify(sessionObject)); }
// function toObj(jwt) { return atob(JSON.parse(jwt)); }
// const fakeUser = {username: "bob@test.com", uid: "1", texp: 3600, tcrt: Date.now()};
// ReactSession.setStoreType("cookie");
//
//

// function App() {
//     // ReactSession.set("__anox_session__", toJWT(fakeUser));
//     if(!ReactSession.get("__anox_session__")) {
//         return (
//             <div>
//                 <LoginComponent registerComp={RegistrationComponent} resetComp={ResetPasswordComponent}/>
//             </div>
//         )
//     }
//     else {
//         const uObj = toObj(ReactSession.get("__anox_session__"));
//         console.log(uObj)
//         return (
//             <div>
//                 <p>Hello, {uObj.username} </p>
//             </div>
//         )
//     }
//
// }
//
// export default App;



// function App() {
//   const [getMessage, setGetMessage] = useState({})
//
//   useEffect(()=>{
//     axios.get('http://localhost:5000/flask/v1/webuser').then(response => {
//       console.log("SUCCESS", response)
//       setGetMessage(response)
//     }).catch(error => {
//       console.log(error)
//     })
//
//   }, [])
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>React + Flask Tutorial</p>
//         <div>{getMessage.status === 200 ?
//           <h3>{getMessage.data.message}</h3>
//           :
//           <h3>LOADING</h3>}</div>
//       </header>
//     </div>
//   );
// }
// export default App;