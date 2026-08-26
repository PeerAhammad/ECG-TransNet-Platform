import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function UploadPage() {
  const [file, setFile]       = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState("")
  const navigate              = useNavigate()

  const handleSubmit = async () => {
    if (!file) return setError("Please select a file.")
    setError(""); setLoading(true)
    try {
      const form = new FormData()
      form.append("file", file)
      const { data } = await api.post("/predict", form)
      const oldHistory = JSON.parse(
  localStorage.getItem('ecg_history') || '[]'
)

const updatedHistory = [data, ...oldHistory].slice(0, 50)

localStorage.setItem(
  'ecg_history',
  JSON.stringify(updatedHistory)
)

navigate("/results", { state: { result: data } })
    } catch (e) {
      setError(e.response?.data?.detail || "Upload failed.")
    } finally { setLoading(false) }
  }

  return (
    <main className="max-w-xl mx-auto px-6 py-20">
      <h1 className="text-3xl font-bold mb-8 text-white">Upload ECG</h1>

      <div className="bg-gray-900 border-2 border-dashed border-gray-700 rounded-2xl p-10 text-center">
        <input type="file" accept=".csv,.txt"
          onChange={e => setFile(e.target.files[0])}
          className="hidden" id="ecg-file" />
        <label htmlFor="ecg-file"
          className="cursor-pointer text-sky-400 hover:text-sky-300 text-lg font-medium">
          {file ? file.name : "Click to select ECG (.csv or .txt)"}
        </label>
      </div>

      {error && <p className="text-red-400 mt-4">{error}</p>}

      <button onClick={handleSubmit} disabled={loading}
        className="mt-6 w-full bg-sky-500 hover:bg-sky-600 disabled:opacity-50 text-white font-semibold py-3 rounded-xl transition">
        {loading ? "Analyzing..." : "Run ECG-TransNet Analysis"}
      </button>
    </main>
  )
}
