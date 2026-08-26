import { useState } from 'react'
import api from '../services/api'

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleLogin = async () => {
    const { data } = await api.post("/login", { email, password })
    localStorage.setItem("token", data.access_token)
    window.location.href = "/upload"
  }

  return (
    <main className="max-w-md mx-auto px-6 py-20">
      <h1 className="text-3xl font-bold mb-8 text-white">Login</h1>
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)}
        className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 mb-4 text-white" />
      <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)}
        className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 mb-6 text-white" />
      <button onClick={handleLogin}
        className="w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 rounded-xl">
        Login
      </button>
    </main>
  )
}
