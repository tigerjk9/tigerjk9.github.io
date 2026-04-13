/* ==========================================================================
   Theme Toggle (Dark / Light)
   ========================================================================== */

(function () {
  var toggle = document.getElementById('theme-toggle');
  if (!toggle) return;

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  toggle.addEventListener('click', function () {
    var current = document.documentElement.getAttribute('data-theme');
    setTheme(current === 'light' ? 'dark' : 'light');
  });
})();
