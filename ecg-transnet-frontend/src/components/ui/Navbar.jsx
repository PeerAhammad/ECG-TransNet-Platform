import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const location = useLocation()

  const links = [
    { name: 'Home', path: '/' },
    { name: 'Analyze ECG', path: '/upload' },
    { name: 'History', path: '/history' },
    { name: 'XAI', path: '/xai' },
  ]

  return (
    <nav className="border-b border-gray-800 bg-gray-950">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">

        {/* Logo */}
        <Link to="/" className="text-xl font-bold text-white">
          ECG<span className="text-sky-400">-TransNet</span>
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-2">
          {links.map(link => {
            const active = location.pathname === link.path

            return (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  active
                    ? 'bg-sky-500/10 text-sky-400'
                    : 'text-gray-400 hover:text-white hover:bg-gray-900'
                }`}
              >
                {link.name}
              </Link>
            )
          })}
        </div>

      </div>
    </nav>
  )
}