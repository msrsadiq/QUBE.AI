import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#17BAA5',
          dark: '#13A08E',
          light: '#1FCDB5',
        },
        secondary: {
          DEFAULT: '#2D3748',
          dark: '#1A202C',
          light: '#4A5568',
        },
        accent: {
          DEFAULT: '#FFFFFF',
          gray: '#F7FAFC',
        },
      },
    },
  },
  plugins: [],
}

export default config