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

/* ===========================================================
   MODAL DE SUPORTE — Formulário de abertura de chamado
   Envio via Formspree (https://formspree.io)
   --------------------------------------------------------
   SETUP NECESSÁRIO (1 vez):
   1. Crie conta grátis em https://formspree.io
   2. Crie um novo form apontando para suporte@nexuserp.com.br
   3. Copie o ID (ex.: "xpwdkgrn") e substitua SEU_FORM_ID abaixo
   =========================================================== */
(function () {
  const FORMSPREE_ID = 'SEU_FORM_ID'; // ← substituir pelo ID do Formspree

  const MODAL_HTML = `
<div id="modal-suporte" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="modal-suporte-title" hidden>
  <div class="modal-box">
    <button class="modal-close" id="modal-close-btn" aria-label="Fechar">✕</button>

    <div class="modal-header">
      <h2 id="modal-suporte-title">Abrir Chamado de Suporte</h2>
      <p>Preencha as informações abaixo e nossa equipe retornará pelo e-mail informado.</p>
    </div>

    <form id="form-suporte" novalidate>
      <div class="modal-form-row">
        <div class="modal-form-group">
          <label for="f-nome">Nome completo *</label>
          <input type="text" id="f-nome" name="nome" required placeholder="Seu nome completo">
        </div>
        <div class="modal-form-group">
          <label for="f-empresa">Empresa *</label>
          <input type="text" id="f-empresa" name="empresa" required placeholder="Nome da empresa">
        </div>
      </div>

      <div class="modal-form-row">
        <div class="modal-form-group">
          <label for="f-email">E-mail para resposta *</label>
          <input type="email" id="f-email" name="email" required placeholder="seu@email.com">
        </div>
        <div class="modal-form-group">
          <label for="f-whatsapp">WhatsApp / Telefone <span class="label-opt">(opcional)</span></label>
          <input type="tel" id="f-whatsapp" name="whatsapp" placeholder="(11) 9 0000-0000">
        </div>
      </div>

      <div class="modal-form-row">
        <div class="modal-form-group">
          <label for="f-modulo">Módulo relacionado</label>
          <select id="f-modulo" name="modulo">
            <option value="">Selecione o módulo...</option>
            <option>Cadastros</option>
            <option>Compras</option>
            <option>Configurações</option>
            <option>Dashboard</option>
            <option>E-commerce &amp; Marketplaces</option>
            <option>Estoque</option>
            <option>Financeiro</option>
            <option>Fiscal</option>
            <option>Relatórios &amp; BI</option>
            <option>Vendas</option>
            <option>Outro / Geral</option>
          </select>
        </div>
        <div class="modal-form-group">
          <label for="f-tipo">Tipo de ocorrência *</label>
          <select id="f-tipo" name="tipo" required>
            <option value="">Selecione...</option>
            <option>Bug / Erro no sistema</option>
            <option>Dúvida de uso</option>
            <option>Lentidão / Instabilidade</option>
            <option>Solicitação de melhoria</option>
            <option>Outro</option>
          </select>
        </div>
      </div>

      <div class="modal-form-group">
        <label for="f-descricao">Descrição do incidente *</label>
        <textarea id="f-descricao" name="descricao" required
          placeholder="Descreva o problema detalhadamente: o que aconteceu, em qual tela, quando ocorreu, quais passos foram realizados..."></textarea>
      </div>

      <div class="modal-form-group">
        <label>Anexos — prints e vídeos <span class="label-opt">Máx. 25 MB por arquivo · até 5 arquivos</span></label>
        <div class="file-drop-zone" id="file-drop-zone" tabindex="0" role="button" aria-label="Clique ou arraste arquivos aqui">
          <input type="file" id="f-anexos" multiple accept="image/*,video/*" style="display:none" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="36" height="36"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          <p class="file-drop-main">Clique ou arraste os arquivos aqui</p>
          <p class="file-drop-hint">Imagens (PNG, JPG, GIF) e vídeos (MP4, MOV) · Vídeos acima de 25 MB: use o campo de link abaixo</p>
        </div>
        <div id="file-list-items" class="file-list-items"></div>
      </div>

      <div class="modal-form-group">
        <label for="f-link">Link de vídeo <span class="label-opt">Google Drive ou YouTube — para vídeos maiores que 25 MB</span></label>
        <input type="url" id="f-link" name="link_video" placeholder="https://drive.google.com/...">
      </div>

      <div id="modal-error" class="modal-msg-error" style="display:none"></div>

      <button type="submit" class="btn-modal-submit" id="btn-modal-submit">
        Enviar Chamado
      </button>
    </form>

    <div id="modal-success" class="modal-success" style="display:none">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="52" height="52"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      <h3>Chamado enviado com sucesso!</h3>
      <p>Nossa equipe receberá suas informações e retornará pelo e-mail informado em até 1 dia útil.</p>
      <button class="btn btn-primary" onclick="fecharModalSuporte()" style="margin-top:8px">Fechar</button>
    </div>
  </div>
</div>`;

  /* ---------- injetar modal no DOM ---------- */
  function injetar() {
    if (document.getElementById('modal-suporte')) return;
    document.body.insertAdjacentHTML('beforeend', MODAL_HTML);
    configurarModal();
  }

  /* ---------- configurar eventos ---------- */
  function configurarModal() {
    const overlay  = document.getElementById('modal-suporte');
    const form     = document.getElementById('form-suporte');
    const dropZone = document.getElementById('file-drop-zone');
    const fileInput= document.getElementById('f-anexos');
    const fileList = document.getElementById('file-list-items');
    let arquivos   = [];

    /* fechar ao clicar no overlay */
    overlay.addEventListener('click', e => { if (e.target === overlay) fecharModalSuporte(); });

    /* fechar ao clicar no X */
    document.getElementById('modal-close-btn').addEventListener('click', fecharModalSuporte);

    /* fechar com Escape */
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !overlay.hasAttribute('hidden')) fecharModalSuporte();
    });

    /* --- drop zone --- */
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); }
    });
    dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', e => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      adicionarArquivos([...e.dataTransfer.files]);
    });
    fileInput.addEventListener('change', () => {
      adicionarArquivos([...fileInput.files]);
      fileInput.value = '';
    });

    function adicionarArquivos(novos) {
      const MAX_MB = 25, MAX_FILES = 5;
      novos.forEach(f => {
        if (arquivos.length >= MAX_FILES) {
          alert('Máximo de ' + MAX_FILES + ' arquivos permitidos.'); return;
        }
        if (f.size > MAX_MB * 1024 * 1024) {
          alert('"' + f.name + '" excede ' + MAX_MB + ' MB.\nPara vídeos grandes, cole o link do Google Drive no campo abaixo.');
          return;
        }
        arquivos.push(f);
      });
      renderizarLista();
    }

    function renderizarLista() {
      fileList.innerHTML = arquivos.map((f, i) => {
        const mb   = (f.size / 1024 / 1024).toFixed(1);
        const icon = f.type.startsWith('video') ? '🎬' : '🖼️';
        return `<div class="file-list-item">
          <span class="file-icon">${icon}</span>
          <span class="file-name">${f.name}</span>
          <span class="file-size">${mb} MB</span>
          <button type="button" class="file-remove" data-idx="${i}" aria-label="Remover ${f.name}">✕</button>
        </div>`;
      }).join('');

      fileList.querySelectorAll('.file-remove').forEach(btn => {
        btn.addEventListener('click', () => {
          arquivos.splice(+btn.dataset.idx, 1);
          renderizarLista();
        });
      });
    }

    /* --- envio do formulário --- */
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const errDiv = document.getElementById('modal-error');
      const btnSub = document.getElementById('btn-modal-submit');

      /* validação nativa */
      if (!form.checkValidity()) { form.reportValidity(); return; }

      if (FORMSPREE_ID === 'SEU_FORM_ID') {
        errDiv.textContent = 'Configuração pendente: substitua SEU_FORM_ID pelo ID do Formspree em main.js.';
        errDiv.style.display = 'block'; return;
      }

      btnSub.disabled = true;
      btnSub.textContent = 'Enviando...';
      errDiv.style.display = 'none';

      const fd = new FormData();
      fd.append('_subject', '🔴 Chamado de Suporte — Nexus ERP');
      fd.append('nome',      document.getElementById('f-nome').value);
      fd.append('empresa',   document.getElementById('f-empresa').value);
      fd.append('email',     document.getElementById('f-email').value);
      fd.append('whatsapp',  document.getElementById('f-whatsapp').value);
      fd.append('modulo',    document.getElementById('f-modulo').value);
      fd.append('tipo',      document.getElementById('f-tipo').value);
      fd.append('descricao', document.getElementById('f-descricao').value);
      fd.append('link_video',document.getElementById('f-link').value);
      arquivos.forEach(f => fd.append('anexo', f));

      try {
        const res = await fetch('https://formspree.io/f/' + FORMSPREE_ID, {
          method: 'POST', headers: { Accept: 'application/json' }, body: fd
        });
        if (res.ok) {
          form.style.display = 'none';
          document.getElementById('modal-success').style.display = 'block';
        } else {
          const data = await res.json().catch(() => ({}));
          errDiv.textContent = (data.errors || []).map(x => x.message).join(' ') || 'Erro ao enviar. Tente novamente.';
          errDiv.style.display = 'block';
        }
      } catch {
        errDiv.textContent = 'Falha na conexão. Verifique sua internet e tente novamente.';
        errDiv.style.display = 'block';
      }

      btnSub.disabled = false;
      btnSub.textContent = 'Enviar Chamado';
    });
  }

  /* ---------- API pública ---------- */
  window.abrirModalSuporte = function () {
    injetar();
    const modal = document.getElementById('modal-suporte');
    modal.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(() => requestAnimationFrame(() => modal.classList.add('open')));
  };

  window.fecharModalSuporte = function () {
    const modal = document.getElementById('modal-suporte');
    if (!modal) return;
    modal.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(() => modal.setAttribute('hidden', ''), 220);
  };
})();
