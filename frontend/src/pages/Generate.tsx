import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { imagesApi, ImageCustomization } from '../api/images';

const Generate: React.FC = () => {
  const navigate = useNavigate();
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  
  // Customization form state
  const [style, setStyle] = useState('elegant');
  const [colorScheme, setColorScheme] = useState('gold');
  const [elements, setElements] = useState('luxury');
  const [mood, setMood] = useState('luxurious');
  const [additionalDetails, setAdditionalDetails] = useState('');
  const [aiModel, setAiModel] = useState('dalle');

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsGenerating(true);

    try {
      const customization: ImageCustomization = {
        style,
        color_scheme: colorScheme,
        elements,
        mood,
        additional_details: additionalDetails || undefined,
      };

      const result = await imagesApi.generate({
        customization,
        ai_model: aiModel,
      });

      // Navigate to dashboard to see the generated image
      navigate('/dashboard', { state: { newImage: result } });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate image. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-yellow-100 to-yellow-200 py-12 px-4">
      <div className="container mx-auto max-w-3xl">
        <div className="bg-white rounded-2xl shadow-2xl p-8" data-testid="generate-form">
          <h1 className="text-4xl font-bold text-center text-gray-800 mb-2">
            Create Your Rich Image
          </h1>
          <p className="text-center text-gray-600 mb-8">
            Customize your AI-generated luxury image (Maximum 5 questions)
          </p>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6" data-testid="error-message">
              {error}
            </div>
          )}

          <form onSubmit={handleGenerate} className="space-y-6">
            {/* Question 1: Style */}
            <div>
              <label className="block text-lg font-semibold text-gray-800 mb-3">
                1. What style do you prefer?
              </label>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {['minimalist', 'maximalist', 'elegant', 'modern', 'classic'].map((s) => (
                  <button
                    key={s}
                    type="button"
                    onClick={() => setStyle(s)}
                    className={`py-3 px-4 rounded-lg font-medium transition capitalize ${
                      style === s
                        ? 'bg-yellow-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                    data-testid={`style-${s}`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            {/* Question 2: Color Scheme */}
            <div>
              <label className="block text-lg font-semibold text-gray-800 mb-3">
                2. Choose your color scheme
              </label>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {[
                  { value: 'gold', label: 'Gold' },
                  { value: 'silver', label: 'Silver' },
                  { value: 'black_gold', label: 'Black & Gold' },
                  { value: 'rose_gold', label: 'Rose Gold' },
                  { value: 'platinum', label: 'Platinum' },
                ].map((c) => (
                  <button
                    key={c.value}
                    type="button"
                    onClick={() => setColorScheme(c.value)}
                    className={`py-3 px-4 rounded-lg font-medium transition ${
                      colorScheme === c.value
                        ? 'bg-yellow-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                    data-testid={`color-${c.value}`}
                  >
                    {c.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Question 3: Elements */}
            <div>
              <label className="block text-lg font-semibold text-gray-800 mb-3">
                3. What elements should be featured?
              </label>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {[
                  { value: 'cars', label: '🚗 Cars' },
                  { value: 'watches', label: '⌚ Watches' },
                  { value: 'jewelry', label: '💎 Jewelry' },
                  { value: 'yachts', label: '🛥️ Yachts' },
                  { value: 'mansions', label: '🏰 Mansions' },
                ].map((e) => (
                  <button
                    key={e.value}
                    type="button"
                    onClick={() => setElements(e.value)}
                    className={`py-3 px-4 rounded-lg font-medium transition ${
                      elements === e.value
                        ? 'bg-yellow-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                    data-testid={`element-${e.value}`}
                  >
                    {e.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Question 4: Mood */}
            <div>
              <label className="block text-lg font-semibold text-gray-800 mb-3">
                4. What mood should it convey?
              </label>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {['luxurious', 'extravagant', 'sophisticated', 'bold', 'subtle'].map((m) => (
                  <button
                    key={m}
                    type="button"
                    onClick={() => setMood(m)}
                    className={`py-3 px-4 rounded-lg font-medium transition capitalize ${
                      mood === m
                        ? 'bg-yellow-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                    data-testid={`mood-${m}`}
                  >
                    {m}
                  </button>
                ))}
              </div>
            </div>

            {/* Question 5: Additional Details */}
            <div>
              <label htmlFor="additionalDetails" className="block text-lg font-semibold text-gray-800 mb-3">
                5. Any additional details? (Optional)
              </label>
              <textarea
                id="additionalDetails"
                value={additionalDetails}
                onChange={(e) => setAdditionalDetails(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
                rows={3}
                placeholder="e.g., Include a private jet, add champagne glasses, make it nighttime..."
                data-testid="additional-details-input"
              />
            </div>

            {/* AI Model Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                AI Model (Advanced)
              </label>
              <select
                value={aiModel}
                onChange={(e) => setAiModel(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
                data-testid="ai-model-select"
              >
                <option value="dalle">DALL-E 3 (OpenAI - Ultra HD, Vertical)</option>
                <option value="dalle2">DALL-E 2 (OpenAI - Fast & Cheap)</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                Configure API keys in backend .env file
              </p>
            </div>

            {/* Generate Button */}
            <div className="pt-6">
              <button
                type="submit"
                disabled={isGenerating}
                className="w-full bg-gradient-to-r from-yellow-500 to-yellow-600 text-white py-4 rounded-xl text-xl font-bold hover:from-yellow-600 hover:to-yellow-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                data-testid="generate-btn"
              >
                {isGenerating ? (
                  <span className="flex items-center justify-center space-x-3">
                    <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    <span>Generating your Rich image...</span>
                  </span>
                ) : (
                  'Generate I\'m Rich Image 🚀'
                )}
              </button>
            </div>
          </form>

          {/* Note about payment */}
          <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-sm text-gray-700 text-center">
              💡 <strong>Note:</strong> Payment integration is prepared for Stripe. 
              Currently generating in demo mode.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Generate;
