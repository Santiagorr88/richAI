import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate('/generate');
    } else {
      navigate('/register');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-yellow-100 to-yellow-200">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="text-center space-y-8">
          {/* Main Title */}
          <h1 className="text-6xl md:text-8xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-700 animate-pulse" data-testid="hero-title">
            💎 I'm Rich AI
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-700 max-w-3xl mx-auto" data-testid="hero-subtitle">
            Generate AI-certified luxury images with a unique serial number.
            <br />
            <span className="font-semibold text-yellow-700">
              Prove your wealth, show your status.
            </span>
          </p>

          {/* Main CTA Button */}
          <div className="pt-8">
            <button
              onClick={handleGetStarted}
              className="bg-gradient-to-r from-yellow-500 to-yellow-600 text-white px-12 py-6 rounded-2xl text-2xl font-bold hover:from-yellow-600 hover:to-yellow-700 transform hover:scale-105 transition-all duration-300 shadow-2xl"
              data-testid="get-started-btn"
            >
              Generate I'm Rich Image 🚀
            </button>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-8 pt-20">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition" data-testid="feature-ai">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">AI-Generated</h3>
              <p className="text-gray-600">
                Powered by Google Gemini for hyper-realistic luxury imagery
              </p>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition" data-testid="feature-unique">
              <div className="text-5xl mb-4">🔒</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Unique Serial</h3>
              <p className="text-gray-600">
                Each image has a unique serial number for authenticity verification
              </p>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition" data-testid="feature-versions">
              <div className="text-5xl mb-4">📱</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">2 Versions</h3>
              <p className="text-gray-600">
                Get a verified version with QR code and a clean wallpaper version
              </p>
            </div>
          </div>

          {/* How It Works */}
          <div className="pt-20">
            <h2 className="text-4xl font-bold text-gray-800 mb-12">How It Works</h2>
            <div className="grid md:grid-cols-4 gap-6">
              <div className="text-center" data-testid="step-1">
                <div className="w-16 h-16 bg-yellow-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  1
                </div>
                <h4 className="font-semibold text-lg mb-2">Customize</h4>
                <p className="text-gray-600 text-sm">Choose your style, colors, and elements</p>
              </div>

              <div className="text-center" data-testid="step-2">
                <div className="w-16 h-16 bg-yellow-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  2
                </div>
                <h4 className="font-semibold text-lg mb-2">Generate</h4>
                <p className="text-gray-600 text-sm">AI creates your unique luxury image</p>
              </div>

              <div className="text-center" data-testid="step-3">
                <div className="w-16 h-16 bg-yellow-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  3
                </div>
                <h4 className="font-semibold text-lg mb-2">Pay</h4>
                <p className="text-gray-600 text-sm">Secure payment with card or Apple Pay</p>
              </div>

              <div className="text-center" data-testid="step-4">
                <div className="w-16 h-16 bg-yellow-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  4
                </div>
                <h4 className="font-semibold text-lg mb-2">Receive</h4>
                <p className="text-gray-600 text-sm">Get your images via email instantly</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
