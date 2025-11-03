/** @type {import('tailwindcss').Config} */

/**
 * Tailwind CSS configuration for Qube.AI
 * 
 * Color Palette: Tarento branding colors
 * - Primary: Teal/Cyan (#14b8a6, #06b6d4)
 * - Accent: Supporting colors for UI elements
 * 
 * Custom Configuration:
 * - Extended color palette for consistent branding
 * - Custom spacing and sizing utilities
 * - Responsive breakpoints
 */

module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Tarento Primary Colors
        primary: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6',  // Main primary color
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        // Accent Colors
        accent: {
          cyan: '#06b6d4',
          teal: '#14b8a6',
          emerald: '#10b981',
        },
        // UI Colors
        background: {
          DEFAULT: '#ffffff',
          secondary: '#f9fafb',
        },
        sidebar: {
          DEFAULT: '#f3f4f6',
          hover: '#e5e7eb',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}