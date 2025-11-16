import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-gradient-to-r from-yellow-500 via-yellow-600 to-yellow-700 shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-white">💎 I'm Rich AI</span>
          </Link>

          <div className="flex items-center space-x-6">
            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  className="text-white hover:text-yellow-200 transition font-medium"
                  data-testid="dashboard-link"
                >
                  My Images
                </Link>
                <div className="flex items-center space-x-3">
                  <span className="text-white text-sm" data-testid="user-email">
                    {user?.email}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="bg-white text-yellow-600 px-4 py-2 rounded-lg hover:bg-yellow-100 transition font-medium"
                    data-testid="logout-button"
                  >
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-white hover:text-yellow-200 transition font-medium"
                  data-testid="login-link"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-white text-yellow-600 px-4 py-2 rounded-lg hover:bg-yellow-100 transition font-medium"
                  data-testid="register-link"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
