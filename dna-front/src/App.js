import React from 'react';
import Warehouse from './components/Warehouse';
import EsMap from './components/EsMap';
import { BrowserRouter, Route, Switch, Link} from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>            
            <Link to="/map">Go to map</Link>
            <Switch>
                <Route path="/" component={Warehouse} exact />
                <Route path="/map" component={EsMap} />
            </Switch>
        </BrowserRouter>
    );
}

export default App;