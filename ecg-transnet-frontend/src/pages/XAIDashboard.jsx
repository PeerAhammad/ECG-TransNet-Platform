export default function XAIDashboard() {
  return (
    <main className="max-w-4xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-bold mb-8 text-white">
        Explainable AI Dashboard
      </h1>

      {/* Explanation */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-6">
        <h2 className="text-xl font-semibold text-white mb-3">
          How ECG-TransNet Makes Predictions
        </h2>

        <p className="text-gray-400 leading-relaxed">
          ECG-TransNet combines a 1D Convolutional Neural Network (CNN)
          with a Transformer encoder. The CNN extracts local ECG
          morphology, while the Transformer captures longer-range
          temporal relationships within the heartbeat signal.
        </p>
      </div>

      {/* Explainability Methods */}
      <div className="grid md:grid-cols-2 gap-5 mb-6">

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <h2 className="text-lg font-semibold text-white mb-3">
            CNN Feature Extraction
          </h2>

          <p className="text-gray-400 text-sm leading-relaxed">
            The CNN identifies important local patterns in the ECG
            waveform such as changes in morphology, peaks and
            waveform characteristics.
          </p>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <h2 className="text-lg font-semibold text-white mb-3">
            Transformer Analysis
          </h2>

          <p className="text-gray-400 text-sm leading-relaxed">
            The Transformer analyzes relationships between different
            parts of the ECG signal to improve the final arrhythmia
            classification.
          </p>
        </div>

      </div>

      {/* Current Status */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <h2 className="text-lg font-semibold text-white mb-3">
          Explainability Status
        </h2>

        <p className="text-gray-400">
          The current platform provides model-level explanations.
          Advanced visualization methods such as SHAP and Grad-CAM
          can be integrated in future versions.
        </p>

        <div className="mt-5 inline-block px-4 py-2 rounded-lg bg-sky-500/10 text-sky-400 text-sm">
          ECG-TransNet-v1.0
        </div>
      </div>
    </main>
  )
}