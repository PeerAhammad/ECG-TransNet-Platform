import { useEffect, useState } from 'react'

const RISK_COLORS = {
  Low: 'text-green-400',
  Medium: 'text-yellow-400',
  High: 'text-orange-400',
  Critical: 'text-red-400',
}

export default function HistoryPage() {
  const [history, setHistory] = useState([])

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem('ecg_history') || '[]')
    setHistory(saved)
  }, [])

  const clearHistory = () => {
    localStorage.removeItem('ecg_history')
    setHistory([])
  }

  return (
    <main className="max-w-6xl mx-auto px-6 py-12">

      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">
            Prediction History
          </h1>
          <p className="text-gray-400 mt-2">
            Previous ECG analysis results
          </p>
        </div>

        {history.length > 0 && (
          <button
            onClick={clearHistory}
            className="px-4 py-2 rounded-lg border border-gray-700
                       text-gray-400 hover:text-red-400
                       hover:border-red-500 transition"
          >
            Clear History
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-12 text-center">
          <h2 className="text-xl font-semibold text-white mb-3">
            No ECG analyses yet
          </h2>

          <p className="text-gray-400">
            Your completed ECG analyses will appear here.
          </p>
        </div>
      ) : (
        <div className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden">

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="border-b border-gray-800">
                <tr>
                  <th className="px-6 py-4 text-sm text-gray-400">
                    File
                  </th>
                  <th className="px-6 py-4 text-sm text-gray-400">
                    Class
                  </th>
                  <th className="px-6 py-4 text-sm text-gray-400">
                    Confidence
                  </th>
                  <th className="px-6 py-4 text-sm text-gray-400">
                    Risk
                  </th>
                  <th className="px-6 py-4 text-sm text-gray-400">
                    Time
                  </th>
                </tr>
              </thead>

              <tbody>
                {history.map((item, index) => (
                  <tr
                    key={item.prediction_id || index}
                    className="border-b border-gray-800 last:border-0 hover:bg-gray-800/40 transition"
                  >
                    <td className="px-6 py-4 text-gray-300">
                      {item.filename || 'ECG file'}
                    </td>

                    <td className="px-6 py-4">
                      <span className="font-semibold text-sky-400">
                        {item.predicted_class}
                      </span>
                    </td>

                    <td className="px-6 py-4 text-gray-300">
                      {(item.confidence * 100).toFixed(1)}%
                    </td>

                    <td
                      className={`px-6 py-4 font-medium ${
                        RISK_COLORS[item.risk_category] || 'text-gray-300'
                      }`}
                    >
                      {item.risk_category}
                    </td>

                    <td className="px-6 py-4 text-gray-500 text-sm">
                      {item.created_at
                        ? new Date(item.created_at).toLocaleString()
                        : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
      )}

    </main>
  )
}