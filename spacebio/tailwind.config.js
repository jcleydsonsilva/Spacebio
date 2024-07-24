//const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
    content: [
        './**/*.html',
        './**/*.js',
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                background: "rgba(var(--background))",
                primary: "rgba(var(--primary))",
                primary2: "rgba(var(--primary-2))",
                secondary: "rgba(var(--secondary))",
                contrast: "rgba(var(--contrast))",
                accent: "rgba(var(--accent))",
                text: "rgba(var(--text))",
                name: "rgba(var(--name))",
                spacepurple1: "rgba(var(--purple1))",
                spacepurple2: "rgba(var(--purple2))",
                spacegreen: "rgba(var(--green))",
                spaceblue: "rgba(var(--blue))",

            },
        },
        keyframes: {
            blob: {
                '0%': { transform: 'translate(0px, 0px) scale(1)' },
                '25%': { transform: 'translate(-40px, -10px) scale(1.1)' },
                '50%': { transform: 'translate(50px, -40px) scale(1.1)' },
                '75%': { transform: 'translate(-20px, 10px) scale(0.9)' },
                '100%': { transform: 'translate(0px, 0px) scale(1)' },
            },

            tilt: {
              "0%, 50%, 100%": { transform: "rotate(0deg)" },
              "25%": { transform: "rotate(0.8deg)" },
              "75%": { transform: "rotate(-0.8deg)" },
            },
            linspin: {
                '100%': { transform: 'rotate(360deg)' },
            },
            easespin: {
                '12.5%': { transform: 'rotate(135deg)' },
                '25%': { transform: 'rotate(270deg)' },
                '37.5%': { transform: 'rotate(405deg)' },
                '50%': { transform: 'rotate(540deg)' },
                '62.5%': { transform: 'rotate(675deg)' },
                '75%': { transform: 'rotate(810deg)' },
                '87.5%': { transform: 'rotate(945deg)' },
                '100%': { transform: 'rotate(1080deg)' },
            },
            'left-spin': {
                '0%': { transform: 'rotate(130deg)' },
                '50%': { transform: 'rotate(-5deg)' },
                '100%': { transform: 'rotate(130deg)' },
            },
            'right-spin': {
                '0%': { transform: 'rotate(-130deg)' },
                '50%': { transform: 'rotate(5deg)' },
                '100%': { transform: 'rotate(-130deg)' },
            },
            rotating: {
                '0%, 100%': { transform: 'rotate(360deg)' },
                '50%': { transform: 'rotate(0deg)' },
            },
            topbottom: {
                '0%, 100%': { transform: 'translate3d(0, -100%, 0)' },
                '50%': { transform: 'translate3d(0, 0, 0)' },
            },
            bottomtop: {
                '0%, 100%': { transform: 'translate3d(0, 0, 0)' },
                '50%': { transform: 'translate3d(0, -100%, 0)' },
            },
        },
        animation: {
            blob: 'blob 8s ease-in-out infinite',
            tilt: 'tilt 5s ease-in-out infinite',
            linspin: 'linspin 1568.2353ms linear infinite',
            easespin: 'easespin 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both',
            'left-spin':
                'left-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both',
            'right-spin':
                'right-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both',
            'ping-once': 'ping 5s cubic-bezier(0, 0, 0.2, 1)',
            rotating: 'rotating 30s linear infinite',
            topbottom: 'topbottom 60s infinite alternate linear',
            bottomtop: 'bottomtop 60s infinite alternate linear',
            'spin-1.5': 'spin 1.5s linear infinite',
            'spin-2': 'spin 2s linear infinite',
            'spin-3': 'spin 3s linear infinite',
        },
    },
    plugins: [],
}
