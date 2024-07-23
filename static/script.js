function getTheme() {
    let htmlTag = document.documentElement;
    return htmlTag.getAttribute('data-bs-theme');
}

function dark() {
    const toggleThemeInput = document.querySelector('.form-check-input');
    const toggleThemeLabel = document.querySelector('.form-check-label');
    const htmlTag = document.documentElement;

    htmlTag.setAttribute('data-bs-theme', 'dark');

    toggleThemeInput.setAttribute('checked', '');
}

function light() {
    const toggleThemeInput = document.querySelector('.form-check-input');
    const toggleThemeLabel = document.querySelector('.form-check-label');
    const htmlTag = document.documentElement;

    htmlTag.setAttribute('data-bs-theme', 'light');

    toggleThemeInput.removeAttribute('checked');
}

function toggleTheme () {
    if (getTheme() === 'dark') {
        light();
    } else {
        dark();
    }
    localStorage.setItem('theme', getTheme());
}

function setTheme(theme) {
    if (theme === 'dark') {
        dark();
    } else {
        light();
    }
}
