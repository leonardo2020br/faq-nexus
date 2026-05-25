/* ===========================================================
   PORTAL NEXUS - Scripts globais
   - Toggle do menu mobile
   - Busca global (filtra cards/links da página atual)
   - Accordion do FAQ
   - Filtro por categoria do FAQ
   =========================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // -------------------------
  // MENU MOBILE
  // -------------------------
  const mobileToggle = document.querySelector('.mobile-toggle');
  const navMain = document.querySelector('.nav-main');
  if (mobileToggle && navMain) {
    mobileToggle.addEventListener('click', () => navMain.classList.toggle('open'));
  }

  // -------------------------
  // DROPDOWN MÓDULOS (mobile: toggle ao clicar no trigger)
  // -------------------------
  const dropdownWrap = document.querySelector('.nav-item-dropdown');
  if (dropdownWrap) {
    const trigger = dropdownWrap.querySelector('.nav-dropdown-trigger');
    // Em touch/mobile, o hover CSS não funciona — usa toggle por clique
    trigger.addEventListener('click', e => {
      const isMobile = window.innerWidth <= 768;
      if (isMobile) {
        e.preventDefault();
        dropdownWrap.classList.toggle('open');
      }
      // Desktop: deixa o href funcionar normalmente (clique vai para /modulos/)
    });
    // Fecha ao clicar fora
    document.addEventListener('click', e => {
      if (!dropdownWrap.contains(e.target)) {
        dropdownWrap.classList.remove('open');
      }
    });
  }

  // -------------------------
  // BUSCA GLOBAL (filtra elementos com [data-search])
  // -------------------------
  const searchInput = document.querySelector('[data-search-input]');
  if (searchInput) {
    searchInput.addEventListener('input', e => {
      const q = e.target.value.toLowerCase().trim();
      document.querySelectorAll('[data-search]').forEach(el => {
        const txt = el.getAttribute('data-search').toLowerCase();
        el.style.display = (!q || txt.includes(q)) ? '' : 'none';
      });
    });
  }

  // Botão "buscar" no hero - redireciona para FAQ com termo
  const heroSearchForm = document.querySelector('[data-hero-search]');
  if (heroSearchForm) {
    heroSearchForm.addEventListener('submit', e => {
      e.preventDefault();
      const term = heroSearchForm.querySelector('input').value.trim();
      if (!term) return;
      window.location.href = `faq.html?q=${encodeURIComponent(term)}`;
    });
  }

  // -------------------------
  // BUSCA NA SIDEBAR DO MÓDULO
  // -------------------------
  const sidebarSearch = document.querySelector('[data-sidebar-search]');
  if (sidebarSearch) {
    const sidebar = sidebarSearch.closest('.doc-sidebar');
    const noResults = sidebar.querySelector('.sidebar-no-results');

    sidebarSearch.addEventListener('input', e => {
      const q = e.target.value.toLowerCase().trim();
      let totalVisible = 0;

      sidebar.querySelectorAll('h4').forEach(h4 => {
        const ul = h4.nextElementSibling;
        if (!ul) return;
        let groupVisible = 0;

        ul.querySelectorAll('li').forEach(li => {
          const text = li.textContent.toLowerCase();
          const match = !q || text.includes(q);
          li.style.display = match ? '' : 'none';
          if (match) groupVisible++;
        });

        h4.style.display = groupVisible > 0 ? '' : 'none';
        ul.style.display = groupVisible > 0 ? '' : 'none';
        totalVisible += groupVisible;
      });

      if (noResults) {
        noResults.style.display = (q && totalVisible === 0) ? 'block' : 'none';
      }
    });
  }

  // -------------------------
  // FAQ - ACCORDION
  // -------------------------
  document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.closest('.faq-item');
      item.classList.toggle('open');
    });
  });

  // -------------------------
  // FAQ - FILTRO POR CATEGORIA
  // -------------------------
  const catButtons = document.querySelectorAll('[data-faq-cat]');
  if (catButtons.length) {
    catButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        catButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.getAttribute('data-faq-cat');
        document.querySelectorAll('.faq-item').forEach(item => {
          const itemCat = item.getAttribute('data-cat');
          item.style.display = (cat === 'todos' || itemCat === cat) ? '' : 'none';
        });
      });
    });
  }

  // -------------------------
  // FAQ - aplica busca da URL (?q=...)
  // -------------------------
  const params = new URLSearchParams(window.location.search);
  const urlQuery = params.get('q');
  const faqSearch = document.querySelector('[data-faq-search]');
  if (urlQuery && faqSearch) {
    faqSearch.value = urlQuery;
    faqSearch.dispatchEvent(new Event('input', { bubbles: true }));
  }
});
