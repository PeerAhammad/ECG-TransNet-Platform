import { Routes, Route } from 'react-router-dom'
import Navbar from './components/ui/Navbar'
import LandingPage    from './pages/LandingPage'
import UploadPage     from './pages/UploadPage'
import ResultsPage    from './pages/ResultsPage'
import HistoryPage    from './pages/HistoryPage'
import XAIDashboard   from './pages/XAIDashboard'
import LoginPage      from './pages/LoginPage'
import RegisterPage   from './pages/RegisterPage'

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Routes>
        <Route path="/"         element={<LandingPage />} />
        <Route path="/upload"   element={<UploadPage />} />
        <Route path="/results"  element={<ResultsPage />} />
        <Route path="/history"  element={<HistoryPage />} />
        <Route path="/xai"      element={<XAIDashboard />} />
        <Route path="/login"    element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </div>
  )
}
