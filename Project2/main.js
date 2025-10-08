// static/js/main.js
document.addEventListener('DOMContentLoaded', ()=> {
  const forms = document.querySelectorAll('form');
  forms.forEach(f => f.addEventListener('submit', ()=> {
    // simple submit visual feedback
    const btn = f.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;
  }));
});