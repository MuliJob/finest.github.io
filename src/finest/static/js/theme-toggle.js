const themeToggle = document.getElementById('theme-toggle');
const lightIcon = document.getElementById('theme-toggle-light-icon');
const darkIcon = document.getElementById('theme-toggle-dark-icon');

if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
    darkIcon.classList.remove('hidden');
    lightIcon.classList.add('hidden');
} else {
    document.documentElement.classList.remove('dark');
    lightIcon.classList.remove('hidden');
    darkIcon.classList.add('hidden');
}

themeToggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const isDarkMode = document.documentElement.classList.contains('dark');

    if (isDarkMode) {
        darkIcon.classList.remove('hidden');
        lightIcon.classList.add('hidden');
        localStorage.setItem('theme', 'dark');
    } else {
        lightIcon.classList.remove('hidden');
        darkIcon.classList.add('hidden');
        localStorage.setItem('theme', 'light');
    }
});
