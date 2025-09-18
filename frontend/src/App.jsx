import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Patients from './pages/Patients'
import Doctors from './pages/Doctors'
import Appointments from './pages/Appointments'
import Dashboard from './pages/Dashboard'
import './index.css'

function App() {
  return (
    <Router>
      <nav style={{ padding: '1rem', backgroundColor: '#f0f0f0' }}>
        <Link to="/" style={{ marginRight: 15 }}>Dashboard</Link>
        <Link to="/patients" style={{ marginRight: 15 }}>Patients</Link>
        <Link to="/doctors" style={{ marginRight: 15 }}>Doctors</Link>
        <Link to="/appointments">Appointments</Link>
      </nav>
      <div style={{ padding: '1rem' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/patients" element={<Patients />} />
          <Route path="/doctors" element={<Doctors />} />
          <Route path="/appointments" element={<Appointments />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
