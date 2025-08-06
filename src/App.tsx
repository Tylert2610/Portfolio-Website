import './App.css';
import TailwindTest from './components/TailwindTest';

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Tailwind Test Component - Remove this after testing */}
      <TailwindTest />

      <header className="bg-gray-800 shadow-lg">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-blue-400">WebbPulse</h1>
            </div>
            <div className="flex items-center space-x-8">
              <a
                href="#about"
                className="text-gray-300 hover:text-blue-400 transition-colors"
              >
                About
              </a>
              <a
                href="#projects"
                className="text-gray-300 hover:text-blue-400 transition-colors"
              >
                Projects
              </a>
              <a
                href="#contact"
                className="text-gray-300 hover:text-blue-400 transition-colors"
              >
                Contact
              </a>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section id="hero" className="text-center py-20">
          <h1 className="text-5xl font-bold mb-6">
            Hi, I'm <span className="text-blue-400">Tyler Webb</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Full-stack developer passionate about creating modern, responsive
            web applications
          </p>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors">
            View My Work
          </button>
        </section>

        <section id="about" className="py-20">
          <h2 className="text-3xl font-bold mb-8 text-center">About Me</h2>
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div>
              <p className="text-gray-300 leading-relaxed">
                I'm a passionate developer with expertise in modern web
                technologies. I love building scalable applications and solving
                complex problems.
              </p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <h3 className="text-xl font-semibold mb-4">Skills</h3>
              <div className="flex flex-wrap gap-2">
                <span className="bg-blue-600 px-3 py-1 rounded-full text-sm">
                  React
                </span>
                <span className="bg-blue-600 px-3 py-1 rounded-full text-sm">
                  TypeScript
                </span>
                <span className="bg-blue-600 px-3 py-1 rounded-full text-sm">
                  Node.js
                </span>
                <span className="bg-blue-600 px-3 py-1 rounded-full text-sm">
                  AWS
                </span>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400">
            &copy; 2024 Tyler Webb. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
