document.addEventListener('DOMContentLoaded', function () {
  const themeToggle = document.getElementById('theme-toggle');

  themeToggle.addEventListener('click', function () {
      const csrftoken = getCookie('csrftoken');

      fetch('/toggle-theme/', {
          method: 'POST',
          headers: {
              'X-CSRFToken': csrftoken,
              'Content-Type': 'application/json',
          },
          credentials: 'same-origin',
      })
          .then(response => response.json())
          .then(data => {
              document.documentElement.setAttribute('data-theme', data.theme);
              document.body.className = `theme-${data.theme}`;

              if (data.theme === 'light') {
                  themeToggle.innerHTML = '<i class="bi bi-moon-fill text-lg"></i>';
              } else {
                  themeToggle.innerHTML = '<i class="bi bi-sun-fill text-lg"></i>';
              }
          })
          .catch(error => {
              console.error('Error:', error);
          });
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
