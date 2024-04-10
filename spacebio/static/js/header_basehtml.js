// load sidenav open or closed from on local storage
window.addEventListener('DOMContentLoaded', function () {
    const sidenav = document.getElementById('sidenav')
    const sidenavState = localStorage.getItem('sidenavOpen')
    const spans = document.querySelectorAll('aside div span')
    if (sidenavState === 'open') {
        sidenav.classList.add('w-48')
        spans.forEach((span) => {
            span.classList.remove('hidden')
            span.classList.remove('opacity-0')
            span.classList.add('opacity-100')
            span.classList.remove('delay-200')
        })
    } else {
        sidenav.classList.add('w-20')
    }
})

// load selected theme from local storage
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('color-theme', theme)
}
// It's best to inline this in `head` to avoid FOUC (flash of unstyled content) when changing pages or themes
if (localStorage.getItem('color-theme') === 'dark' || (!localStorage.getItem('color-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    setTheme('dark')
} else {
    setTheme('light')
}


// Update sidenav and mobile menu icons based on current page
function updateIconsBasedOnPage() {
    const links = document.querySelectorAll('#sideItems a, #mobile-menu a')
    const windowPath = window.location.pathname

    links.forEach((link) => {
        const icon = link.querySelector('i')
        const span = link.querySelector('span')
        const linkUrl = link.getAttribute('href')

        if (windowPath == linkUrl) {
            icon.classList.remove('text-text')
            span.classList.remove('text-text')
            icon.classList.add('text-spacepurple2')
            span.classList.add('text-spacepurple2')
        } else {
            icon.classList.remove('text-spacepurple2')
            span.classList.remove('text-spacepurple2')
            icon.classList.add('text-text')
            span.classList.add('text-text')
        }
    })
}
window.addEventListener('DOMContentLoaded', updateIconsBasedOnPage)