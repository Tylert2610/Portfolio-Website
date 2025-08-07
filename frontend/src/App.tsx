import { useState, useEffect } from 'react';
import { Home } from './pages';
import { AdminPanel } from './components/admin/AdminPanel';
import './styles/globals.css';

function App() {
  const [showAdmin, setShowAdmin] = useState(false);

  useEffect(() => {
    // Check if admin parameter is in URL
    const urlParams = new URLSearchParams(window.location.search);
    const isAdmin = urlParams.get('admin') === 'true';
    setShowAdmin(isAdmin);
  }, []);

  if (showAdmin) {
    return <AdminPanel />;
  }

  return (
    <div className="App">
      <Home />
    </div>
  );
}

export default App;
