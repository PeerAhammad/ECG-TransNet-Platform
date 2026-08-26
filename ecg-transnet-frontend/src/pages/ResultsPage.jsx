import { useLocation, Link } from 'react-router-dom'

const RISK_COLORS = {
  Low: "text-green-400",
  Medium: "text-yellow-400",
  High: "text-orange-400",
  Critical: "text-red-400"
}

const CLASS_NAMES = {
  N: "Normal Beat",
  S: "Supraventricular Ectopic",
  V: "Ventricular Ectopic",
  F: "Fusion Beat",
  Q: "Unknown / Paced Beat"
}

const CLASS_COLORS = {
  N: "bg-green-500",
  S: "bg-yellow-500",
  V: "bg-orange-500",
  F: "bg-purple-500",
  Q: "bg-red-500"
}

export default function ResultsPage() {
  const { state } = useLocation()
  const r = state?.result

  if (!r) {
    return (
      <div className="text-center py-20 text-gray-400">
        <p>No result found.</p>
        <Link to="/upload" className="text-sky-400 hover:text-sky-300">
          Upload ECG
        </Link>
      </div>
    )
  }

  return (
    <main className="max-w-4xl mx-auto px-6 py-12">

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">
          Analysis Results
        </h1>

        <p className="text-gray-400 mt-2">
          ECG-TransNet arrhythmia classification
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">

        {/* Predicted Class */}
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
          <p className="text-gray-400 text-sm">
            Predicted Class
          </p>

          <p className="text-3xl font-bold mt-2 text-white">
            {r.predicted_class}
          </p>

          <p className="text-gray-400 mt-1">
            {r.class_name || CLASS_NAMES[r.predicted_class]}
          </p>
        </div>

        {/* Confidence */}
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
          <p className="text-gray-400 text-sm">
            Confidence
          </p>

          <p className="text-3xl font-bold mt-2 text-white">
            {(r.confidence * 100).toFixed(1)}%
          </p>
        </div>

        {/* Risk */}
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
          <p className="text-gray-400 text-sm">
            Risk Category
          </p>

          <p
            className={`text-3xl font-bold mt-2 ${
              RISK_COLORS[r.risk_category] || "text-white"
            }`}
          >
            {r.risk_category}
          </p>
        </div>

        {/* Processing Time */}
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
          <p className="text-gray-400 text-sm">
            Processing Time
          </p>

          <p className="text-3xl font-bold mt-2 text-white">
            {r.processing_time_seconds}s
          </p>
        </div>

      </div>

      {/* ECG Analysis Summary */}
      <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800 mb-8">

        <h2 className="text-xl font-semibold text-white mb-5">
          ECG Analysis Summary
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

          <div>
            <p className="text-sm text-gray-500">
              Beats Analysed
            </p>

            <p className="text-xl font-semibold text-white mt-1">
              {r.n_beats_analysed}
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">
              Model Version
            </p>

            <p className="text-xl font-semibold text-white mt-1">
              {r.model_version}
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">
              Predicted Rhythm
            </p>

            <p className="text-xl font-semibold text-white mt-1">
              {r.class_name || CLASS_NAMES[r.predicted_class]}
            </p>
          </div>

        </div>

      </div>

      {/* Class Probabilities */}
      <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800 mb-8">

        <h2 className="text-xl font-semibold text-white mb-5">
          Class Probabilities
        </h2>

        {Object.entries(r.class_probabilities).map(([cls, prob]) => (

          <div key={cls} className="mb-5">

            <div className="flex items-center justify-between mb-2">

              <div>
                <span className="text-gray-300 font-medium">
                  {cls}
                </span>

                <span className="text-gray-500 text-sm ml-3">
                  {CLASS_NAMES[cls]}
                </span>
              </div>

              <span className="text-gray-300">
                {(prob * 100).toFixed(1)}%
              </span>

            </div>

            <div className="w-full bg-gray-800 rounded-full h-3">

              <div
                className={`${CLASS_COLORS[cls] || "bg-sky-500"} h-3 rounded-full transition-all duration-500`}
                style={{
                  width: `${Math.max(prob * 100, prob > 0 ? 0.5 : 0)}%`
                }}
              />

            </div>

          </div>

        ))}

      </div>

      {/* Per-Beat Analysis */}
      {r.per_beat_classes && r.per_beat_classes.length > 0 && (

        <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800 mb-8">

          <h2 className="text-xl font-semibold text-white mb-2">
            Per-Beat Analysis
          </h2>

          <p className="text-gray-500 text-sm mb-6">
            Individual beat classifications produced by ECG-TransNet.
          </p>

          {/* Timeline */}
          <div className="flex flex-wrap gap-3">

            {r.per_beat_classes.map((cls, index) => (

              <div
                key={index}
                className="flex flex-col items-center"
              >

                <div
                  className={`w-12 h-12 rounded-lg flex items-center justify-center text-white font-bold ${
                    CLASS_COLORS[cls] || "bg-gray-700"
                  }`}
                >
                  {cls}
                </div>

                <span className="text-xs text-gray-500 mt-2">
                  Beat {index + 1}
                </span>

              </div>

            ))}

          </div>

          {/* Legend */}
          <div className="flex flex-wrap gap-5 mt-7 pt-5 border-t border-gray-800">

            {Object.entries(CLASS_NAMES).map(([cls, name]) => (

              <div
                key={cls}
                className="flex items-center gap-2"
              >

                <span
                  className={`w-3 h-3 rounded-full ${
                    CLASS_COLORS[cls] || "bg-gray-700"
                  }`}
                />

                <span className="text-xs text-gray-400">
                  {cls} — {name}
                </span>

              </div>

            ))}

          </div>

        </div>

      )}

      {/* Prediction Information */}
      <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800">

        <h2 className="text-lg font-semibold text-white mb-4">
          Prediction Information
        </h2>

        <div className="space-y-3 text-sm">

          <div className="flex flex-col sm:flex-row sm:justify-between gap-1">
            <span className="text-gray-500">
              Prediction ID
            </span>

            <span className="text-gray-400 font-mono text-xs">
              {r.prediction_id}
            </span>
          </div>

          <div className="flex justify-between">
            <span className="text-gray-500">
              Model
            </span>

            <span className="text-gray-400">
              {r.model_version}
            </span>
          </div>

          <div className="flex justify-between">
            <span className="text-gray-500">
              Beats Analysed
            </span>

            <span className="text-gray-400">
              {r.n_beats_analysed}
            </span>
          </div>

        </div>

      </div>

      {/* Actions */}
      <div className="flex gap-4 mt-8">

        <Link
          to="/upload"
          className="flex-1 text-center bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 rounded-xl transition"
        >
          Analyze Another ECG
        </Link>

      </div>

    </main>
  )
}