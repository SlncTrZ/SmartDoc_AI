module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0056b3',
        success: '#28a745',
        warning: '#ffc107',
        background: '#f8f9fa',
      },
      fontSize: {
        'base': ['14px', '1.5'],
        'lg': ['16px', '1.6'],
        'xl': ['18px', '1.7'],
      }
    },
  },
  plugins: [],
}
