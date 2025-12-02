module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    darkMode: 'class',
    theme: {
        extend: {
            fontFamily: {
                sans: ['"Geist Sans"', 'sans-serif'],
                mono: ['"Geist Mono"', 'monospace'],
            },
            fontSize: {
                'xs': ['0.75rem', { lineHeight: '1rem', letterSpacing: '0' }],
                'sm': ['0.875rem', { lineHeight: '1.25rem', letterSpacing: '0' }],
                'base': ['1rem', { lineHeight: '1.5rem', letterSpacing: '-0.01em' }],
                'lg': ['1.5rem', { lineHeight: '1.75rem', letterSpacing: '-0.02em', fontWeight: '600' }],
                'xl': ['2rem', { lineHeight: '2.25rem', letterSpacing: '-0.02em', fontWeight: '700' }],
                '2xl': ['3rem', { lineHeight: '1', letterSpacing: '-0.03em', fontWeight: '800' }],
                '3xl': ['4rem', { lineHeight: '1', letterSpacing: '-0.04em', fontWeight: '800' }],
            },
            letterSpacing: {
                tighter: '-0.05em',
                tight: '-0.02em',
                normal: '-0.01em',
                wide: '0.02em',
            },
            colors: {
                gray: {
                    50: '#f9fafb',
                    100: '#fafafa', // App Background
                    200: '#eaeaea', // Borders
                    300: '#999999', // Subtle Text
                    400: '#888888', // Secondary Text
                    500: '#666666', // Icons / Meta
                    600: '#444444',
                    700: '#333333',
                    800: '#111111', // Dark Accents
                    900: '#000000', // Headings
                },
                blue: {
                    geist: '#0070f3', // Primary Brand
                    dark: '#0761d1',
                    light: '#3291ff',
                },
                red: {
                    geist: '#e00000', // Error
                    light: '#ff1a1a',
                    dark: '#c50000',
                },
                amber: {
                    geist: '#f5a623', // Warning
                    400: '#f5a623',
                },
                violet: {
                    geist: '#7928ca', // Beta/Feature
                },
                cyan: {
                    geist: '#50e3c2', // Success
                },
            },
            boxShadow: {
                'geist': '0 0 0 1px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.04)',
                'geist-hover': '0 0 0 1px rgba(0,0,0,0.08), 0 6px 14px rgba(0,0,0,0.08)',
                'geist-active': '0 0 0 1px #000',
            },
            borderRadius: {
                'geist': '6px',
            }
        }
    },
    plugins: [],
}
