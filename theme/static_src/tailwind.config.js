module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    safelist: [
        'bg-yellow-200',
        'bg-orange-500',
        'bg-green-500',
        'bg-blue-500',
        'bg-amber-800',
        'bg-black',
        'bg-yellow-100',
        'bg-orange-100',
        'bg-green-100',
        'bg-blue-100',
        'bg-amber-100',
        'bg-stone-200',
        'ring-2',
        'ring-yellow-400',
        'ring-orange-400',
        'ring-green-500',
        'ring-blue-400',
        'ring-amber-700',
        'ring-stone-500',
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    red: '#C8102E',
                    'red-dark': '#9E0C24',
                    blue: '#1B4F9C',
                    'blue-dark': '#143A74',
                    'blue-light': '#E8F0FA',
                },
                ink: '#1A1A1A',
                muted: '#5C5C5C',
            },
            fontFamily: {
                sans: ['"Barlow Condensed"', 'Arial Narrow', 'system-ui', 'sans-serif'],
                display: ['"Barlow Condensed"', 'Arial Narrow', 'system-ui', 'sans-serif'],
                condensed: ['"Barlow Condensed"', 'Arial Narrow', 'system-ui', 'sans-serif'],
                body: ['system-ui', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
            },
            // Condensed face reads smaller than regular sans — bumped sports/marketing scale
            fontSize: {
                xs: ['0.8125rem', { lineHeight: '1.25rem', letterSpacing: '0.02em' }],
                sm: ['0.9375rem', { lineHeight: '1.5rem', letterSpacing: '0.015em' }],
                base: ['1.125rem', { lineHeight: '1.75rem', letterSpacing: '0.01em' }],
                lg: ['1.25rem', { lineHeight: '1.9rem', letterSpacing: '0.01em' }],
                xl: ['1.5rem', { lineHeight: '2rem', letterSpacing: '0.005em' }],
                '2xl': ['1.75rem', { lineHeight: '2.15rem' }],
                '3xl': ['2.125rem', { lineHeight: '2.4rem' }],
                '4xl': ['2.625rem', { lineHeight: '1.15' }],
                '5xl': ['3.25rem', { lineHeight: '1.1' }],
                '6xl': ['4rem', { lineHeight: '1.05' }],
                '7xl': ['4.75rem', { lineHeight: '1' }],
                '8xl': ['6rem', { lineHeight: '1' }],
                '9xl': ['7.5rem', { lineHeight: '1' }],
            },



            borderRadius: {
                brand: '0.75rem',
            },
            maxWidth: {
                content: '64rem',
            },
            keyframes: {
                'fade-up': {
                    '0%': { opacity: '0', transform: 'translateY(1rem)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                'fade-in': {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
            },
            animation: {
                'fade-up': 'fade-up 0.7s ease-out both',
                'fade-in': 'fade-in 0.6s ease-out both',
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
