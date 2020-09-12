import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [ping, setPing] = useState({msg: 'ping'});
  const HOST = 'http://localhost:8000'

  return (
    <div className="App">
      <header className="App-header">
        <input type="text" value={ping.msg} onChange={
            (e) => {
                setPing({msg: e.target.value})
            }
        }/>
        <button onClick={
            () => {
                axios.post(`${HOST}/ping`, ping)
                .then(function (response) {
                    alert(response.data);
                }).catch(function (error) {
                    console.error(error);
                });
            }
        }>
        Send Ping
        </button>
      </header>
    </div>
  );
}

export default App;