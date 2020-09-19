import React from 'react';
import Warehouse from './components/Warehouse';
import EsMap from './components/EsMap';
import { Route, Switch } from 'react-router-dom';

function App() {
    return (
        <main>
            <Switch>
                <Route path="/" component={Warehouse} exact />
                <Route path="/map" component={EsMap} />
            </Switch>
        </main>
    )
}

export default App;