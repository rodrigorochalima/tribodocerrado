/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f97316',
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
        },
        dark: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        }
      },
      fontFamily: {
        'metal': ['Cinzel', 'serif'],
      },
      animation: {
        'fire': 'fire 2s ease-in-out infinite alternate',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        fire: {
          '0%': { 
            boxShadow: '0 0 20px #ff6b35, 0 0 40px #ff6b35, 0 0 60px #ff6b35',
            transform: 'scale(1)'
          },
          '100%': { 
            boxShadow: '0 0 30px #ff8c42, 0 0 60px #ff8c42, 0 0 90px #ff8c42',
            transform: 'scale(1.05)'
          }
        },
        glow: {
          '0%': { 
            textShadow: '0 0 10px #ff6b35, 0 0 20px #ff6b35, 0 0 30px #ff6b35'
          },
          '100%': { 
            textShadow: '0 0 20px #ff8c42, 0 0 30px #ff8c42, 0 0 40px #ff8c42'
          }
        }
      }
    },
  },
  plugins: [],
}
