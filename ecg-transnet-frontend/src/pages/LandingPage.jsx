import { Link } from 'react-router-dom'

export default function LandingPage() {
  return (
    <main>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 py-24 text-center">

        <div className="inline-block px-4 py-2 rounded-full bg-sky-500/10 text-sky-400 text-sm mb-6">
          AI-Powered ECG Analysis
        </div>

        <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight">
          Intelligent ECG
          <span className="text-sky-400"> Arrhythmia Detection</span>
        </h1>

        <p className="max-w-2xl mx-auto mt-6 text-lg text-gray-400 leading-relaxed">
          ECG-TransNet uses a hybrid CNN-Transformer architecture
          to analyze ECG signals and classify cardiac rhythms
          quickly and automatically.
        </p>

        {/* Buttons */}
        <div className="flex justify-center gap-4 mt-10">

          <Link
            to="/upload"
            className="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-600 text-white font-semibold transition"
          >
            Analyze ECG
          </Link>

          <Link
            to="/xai"
            className="px-6 py-3 rounded-xl border border-gray-700 hover:border-gray-500 text-gray-300 hover:text-white font-semibold transition"
          >
            Explore XAI
          </Link>

        </div>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-6 pb-20">

        <div className="grid md:grid-cols-3 gap-5">

          <Feature
            title="ECG Preprocessing"
            text="Signal filtering, normalization, R-peak detection and heartbeat segmentation."
          />

          <Feature
            title="CNN + Transformer"
            text="CNN extracts local ECG morphology while the Transformer captures temporal relationships."
          />

          <Feature
            title="Explainable Results"
            text="View predicted rhythm, confidence, risk category and model explanations."
          />

        </div>

      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-6 text-center text-sm text-gray-600">
        ECG-TransNet • Hybrid CNN-Transformer ECG Analysis
      </footer>

    </main>
  )
}

function Feature({ title, text }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
      <h2 className="text-lg font-semibold text-white mb-3">
        {title}
      </h2>

      <p className="text-sm text-gray-400 leading-relaxed">
        {text}
      </p>
    </div>
  )
}