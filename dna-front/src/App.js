import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [storeInfo, setStoreInfo] = useState({
      store: 'jongno',
      product: 'Apple watch series 6'
  });
//   const HOST = 'http://localhost:8000';
  const HOST = 'https://l155m9dcql.execute-api.ap-northeast-2.amazonaws.com/api';

  return (
    <div className="App">
      <header className="App-header">
        <select onChange={
            (e) => {
                const value = e.target.value;
                setStoreInfo(preState => {
                    return {...preState, store: value}
                });
            }
        }>
            <option value="jongno">종로</option>
            <option value="gangnam">강남</option>
            <option value="pangyo">판교</option>
        </select>
        <input type="text" value={storeInfo.product} onChange={
            (e) => {
                const value = e.target.value;
                setStoreInfo(preState => {
                    return {...preState, product: value}
                });
            }
        }/>
        <button onClick={
            () => {
                axios.post(`${HOST}/warehouse`, storeInfo)
                .then(function (response) {
                    alert(response.data);
                }).catch(function (error) {
                    console.error(error);
                });
            }
        }>
        신상입고
        </button>
      </header>
    </div>
  );
}

export default App;