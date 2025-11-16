import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { imagesApi, ImageData } from '../api/images';
import { useAuth } from '../context/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const location = useLocation();
  const [images, setImages] = useState<ImageData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [copiedSerial, setCopiedSerial] = useState<string | null>(null);

  useEffect(() => {
    loadImages();
  }, []);

  const loadImages = async () => {
    try {
      const data = await imagesApi.getMyImages();
      setImages(data);
    } catch (err: any) {
      setError('Failed to load images');
    } finally {
      setIsLoading(false);
    }
  };

  const copySerial = (serial: string) => {
    navigator.clipboard.writeText(serial);
    setCopiedSerial(serial);
    setTimeout(() => setCopiedSerial(null), 2000);
  };

  const downloadImage = (url: string, filename: string) => {
    const link = document.createElement('a');
    link.href = `http://localhost:8001${url}`;
    link.download = filename;
    link.click();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-yellow-100 to-yellow-200 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-yellow-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-yellow-100 to-yellow-200 py-12 px-4">
      <div className="container mx-auto">
        <div className="mb-8" data-testid="dashboard-header">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            My Rich Images 💼
          </h1>
          <p className="text-gray-600">
            Welcome back, {user?.first_name || user?.email}! Here are all your generated images.
          </p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {images.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-lg p-12 text-center" data-testid="no-images">
            <div className="text-6xl mb-4">🖼️</div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">No images yet</h3>
            <p className="text-gray-600 mb-6">
              You haven't generated any I'm Rich images yet.
            </p>
            <a
              href="/generate"
              className="inline-block bg-gradient-to-r from-yellow-500 to-yellow-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-yellow-600 hover:to-yellow-700 transition"
              data-testid="generate-first-image-btn"
            >
              Generate Your First Image
            </a>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {images.map((image) => (
              <div
                key={image.id}
                className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition"
                data-testid={`image-card-${image.serial}`}
              >
                {/* Image Preview */}
                <div className="relative aspect-[9/16] bg-gray-200">
                  <img
                    src={`http://localhost:8001${image.image_url_wallpaper}`}
                    alt={`Rich image ${image.serial}`}
                    className="w-full h-full object-cover"
                    data-testid="image-preview"
                  />
                </div>

                {/* Image Details */}
                <div className="p-6 space-y-4">
                  {/* Serial Number */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-semibold text-gray-600">Serial Number</span>
                      <button
                        onClick={() => copySerial(image.serial)}
                        className="text-xs bg-yellow-100 text-yellow-700 px-3 py-1 rounded hover:bg-yellow-200 transition"
                        data-testid="copy-serial-btn"
                      >
                        {copiedSerial === image.serial ? '✓ Copied!' : 'Copy'}
                      </button>
                    </div>
                    <p className="font-mono text-sm text-gray-800 break-all" data-testid="serial-number">
                      {image.serial}
                    </p>
                  </div>

                  {/* Created Date */}
                  <div>
                    <span className="text-sm font-semibold text-gray-600">Created</span>
                    <p className="text-sm text-gray-800">
                      {new Date(image.created_at).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </p>
                  </div>

                  {/* Payment Status */}
                  <div>
                    <span className="text-sm font-semibold text-gray-600">Status</span>
                    <p className="text-sm">
                      <span
                        className={`inline-block px-2 py-1 rounded text-xs font-semibold ${
                          image.payment_status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                        data-testid="payment-status"
                      >
                        {image.payment_status}
                      </span>
                    </p>
                  </div>

                  {/* Action Buttons */}
                  <div className="space-y-2 pt-2">
                    <button
                      onClick={() => downloadImage(image.image_url_wallpaper, `${image.serial}_wallpaper.jpg`)}
                      className="w-full bg-yellow-500 text-white py-2 rounded-lg hover:bg-yellow-600 transition font-medium"
                      data-testid="download-wallpaper-btn"
                    >
                      📱 Download Wallpaper
                    </button>
                    <button
                      onClick={() => downloadImage(image.image_url_verified, `${image.serial}_verified.jpg`)}
                      className="w-full bg-gray-700 text-white py-2 rounded-lg hover:bg-gray-800 transition font-medium"
                      data-testid="download-verified-btn"
                    >
                      🔒 Download Verified (QR)
                    </button>
                    <a
                      href={`/verify/${image.serial}`}
                      className="block w-full bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 transition text-center font-medium"
                      data-testid="verify-btn"
                    >
                      ✓ Verify Authenticity
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
