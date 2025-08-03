import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Requirements from './pages/Requirements'
import UserStories from './pages/UserStories'
import Design from './pages/Design'
import Code from './pages/Code'
import Testing from './pages/Testing'
import ReviewHistory from './pages/ReviewHistory'

function App() {
  return (
    <>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/requirements" element={<Requirements />} />
            <Route path="/user-stories" element={<UserStories />} />
            <Route path="/design" element={<Design />} />
            <Route path="/code" element={<Code />} />
            <Route path="/testing" element={<Testing />} />
            <Route path="/history" element={<ReviewHistory />} />
          </Routes>
        </Layout>
      </Router>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          className: 'text-sm',
        }}
      />
    </>
  )
}

export default App