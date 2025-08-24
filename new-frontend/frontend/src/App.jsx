

import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import 'chartjs-adapter-date-fns';


import Dashboard from './components/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <div>
        <h1>Sensor Dashboard</h1>
        <p>Time-series sensor data and correlation analysis</p>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          
          
        </Routes>
      </div>
    </BrowserRouter>
  );
}


// import './App.css';
// import Dashboard from './components/Dashboard';

// function App() {
//   return (
//     <div>
//       <h1>Sensor Dashboard</h1>
//       <p>Time-series sensor data and correlation analysis</p>
//       <Dashboard />
//     </div>
//   );
// }


export default App;