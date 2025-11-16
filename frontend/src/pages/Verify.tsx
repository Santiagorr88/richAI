import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { imagesApi, VerifyResponse } from '../api/images';

const Verify: React.FC = () => {
  const { serial: urlSerial } = useParams<{ serial: string }>();
  const [serial, setSerial] = useState(urlSerial || '');
  const [result, setResult] = useState<VerifyResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasVerified, setHasVerified] = useState(false);

  useEffect(() => {
    if (urlSerial) {
      verifySerial(urlSerial);
    }
  }, [urlSerial]);

  const verifySerial = async (serialToVerify: string) => {
    setIsLoading(true);
    setHasVerified(false);
    try {
      const data = await imagesApi.verify(serialToVerify);
      setResult(data);
      setHasVerified(true);
    } catch (err) {
      setResult({ valid: false });
      setHasVerified(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    if (serial.trim()) {
      verifySerial(serial.trim());
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-yellow-100 to-yellow-200 py-12 px-4">
      <div className="container mx-auto max-w-2xl">
        <div className="bg-white rounded-2xl shadow-2xl p-8" data-testid="verify-page">
          <h1 className="text-4xl font-bold text-center text-gray-800 mb-2">
            Verify Image Authenticity
          </h1>
          <p className="text-center text-gray-600 mb-8">
            Enter a serial number to verify if an I'm Rich image is authentic
          </p>

          {/* Verification Form */}
          <form onSubmit={handleVerify} className="mb-8">
            <div className="flex space-x-3">
              <input
                type="text"
                value={serial}
                onChange={(e) => setSerial(e.target.value)}
                placeholder="Enter serial number (e.g., RICH-20241116-XXXXXXXX)"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
                data-testid="serial-input"
              />
              <button
                type="submit"
                disabled={isLoading || !serial.trim()}
                className="bg-gradient-to-r from-yellow-500 to-yellow-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-yellow-600 hover:to-yellow-700 transition disabled:opacity-50"
                data-testid="verify-btn"
              >
                {isLoading ? 'Verifying...' : 'Verify'}
              </button>
            </div>
          </form>

          {/* Verification Result */}
          {hasVerified && result && (
            <div data-testid="verification-result">
              {result.valid ? (
                <div className="bg-green-50 border-2 border-green-500 rounded-xl p-8 text-center">
                  <div className="text-6xl mb-4">✅</div>
                  <h2 className="text-3xl font-bold text-green-800 mb-4">Authentic Image</h2>
                  <p className="text-green-700 mb-6">
                    This image is registered in our database and is authentic.
                  </p>

                  <div className="space-y-4 text-left bg-white p-6 rounded-lg">
                    <div>
                      <span className="font-semibold text-gray-700">Serial Number:</span>
                      <p className="font-mono text-sm text-gray-900 mt-1" data-testid="verified-serial">{result.serial}</p>
                    </div>

                    {result.created_at && (
                      <div>
                        <span className="font-semibold text-gray-700">Created:</span>
                        <p className="text-gray-900 mt-1">
                          {new Date(result.created_at).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit',
                          })}
                        </p>
                      </div>
                    )}

                    {result.user_email && (
                      <div>
                        <span className="font-semibold text-gray-700">Owner:</span>
                        <p className="text-gray-900 mt-1">{result.user_email}</p>
                      </div>
                    )}
                  </div>

                  {result.image_url_verified && (
                    <div className="mt-6">
                      <img
                        src={`http://localhost:8001${result.image_url_verified}`}
                        alt="Verified image"
                        className="max-w-md mx-auto rounded-lg shadow-lg"
                        data-testid="verified-image"
                      />
                    </div>
                  )}
                </div>
              ) : (
                <div className="bg-red-50 border-2 border-red-500 rounded-xl p-8 text-center" data-testid="invalid-result">
                  <div className="text-6xl mb-4">❌</div>
                  <h2 className="text-3xl font-bold text-red-800 mb-4">Not Authentic</h2>
                  <p className="text-red-700">
                    This serial number is not registered in our database.
                    <br />
                    This image may be fake or the serial number is incorrect.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Info Section */}
          <div className="mt-8 p-6 bg-yellow-50 border border-yellow-200 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">💡 How Verification Works</h3>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>• Each I'm Rich image has a unique serial number</li>
              <li>• Serial numbers are stored in our secure database</li>
              <li>• QR codes on verified images link directly to this page</li>
              <li>• Only authentic images will show as verified</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Verify;
