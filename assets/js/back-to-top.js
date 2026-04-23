(function () {
  var btn = document.createElement('button');
  btn.id = 'back-to-top';
  btn.setAttribute('aria-label', '맨 위로');
  btn.innerHTML = '<i class="fas fa-chevron-up"></i>';
  document.body.appendChild(btn);

  window.addEventListener('scroll', function () {
    if (window.scrollY > 300) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
