// ═══════════════════════════════════════════════════
//  BUS CONCIERTOS — JavaScript Principal
// ═══════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {

  // ─── Navbar responsive toggle ───────────────────
  const toggler = document.querySelector('.navbar-toggler');
  const collapse = document.querySelector('.nav-collapse');
  if (toggler && collapse) {
    toggler.addEventListener('click', () => {
      collapse.classList.toggle('open');
    });
  }

  // ─── Cerrar alertas automáticamente ────────────
  document.querySelectorAll('.alert[data-auto-dismiss]').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

  // ─── Confirmar eliminaciones ─────────────────────
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (!confirm(btn.dataset.confirm || '¿Estás seguro de esta acción?')) {
        e.preventDefault();
      }
    });
  });

  // ─── Formatear RUT mientras se escribe ──────────
  const rutInput = document.querySelector('input[name="rut"]');
  if (rutInput) {
    rutInput.addEventListener('input', (e) => {
      let val = e.target.value.replace(/[^0-9kK]/g, '');
      if (val.length > 1) {
        const cuerpo = val.slice(0, -1);
        const dv = val.slice(-1);
        const cuerpoFormateado = cuerpo.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        e.target.value = `${cuerpoFormateado}-${dv}`;
      } else {
        e.target.value = val;
      }
    });
  }

  // ─── Animación de aparición al hacer scroll ──────
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

  // ─── Tooltip WhatsApp ────────────────────────────
  const waFab = document.querySelector('.whatsapp-fab');
  if (waFab) {
    waFab.addEventListener('mouseenter', () => {
      const tooltip = waFab.querySelector('.tooltip-wa');
      if (tooltip) tooltip.style.opacity = '1';
    });
    waFab.addEventListener('mouseleave', () => {
      const tooltip = waFab.querySelector('.tooltip-wa');
      if (tooltip) tooltip.style.opacity = '0';
    });
  }

  // ─── Resaltar enlace activo en navbar ────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

});

// ─── Función global: formatear precio CLP ──────────
function formatPrecio(valor) {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    minimumFractionDigits: 0
  }).format(valor);
}
