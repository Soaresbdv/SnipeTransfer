const { createApp } = Vue;

createApp({
  data() {
    return {
      mode: 'form',
      search: '',
      suggestions: [],
      selectedUser: null,
      showSuggestions: false,
      assetNumber: '',
      editIndex: null,
      editUsername: '',
      editAsset: '',
      vinculos: [],
      notification: { show: false, message: '', type: 'info' }, 
      duplicatePrompt: { show: false, tag: '', user: '', owners: [] } 
    };
  },
  mounted() {
    const toggle = document.getElementById("theme-toggle");
    const root = document.documentElement;
    const saved = localStorage.getItem("theme");

    const applyLight = () => {
      root.classList.remove("dark");
      document.body.classList.add("light-theme");
      document.body.classList.remove("bg-gradient-to-br","from-indigo-600","via-indigo-700","to-violet-700");
      document.body.classList.add("bg-[#f8f4f0]");
    };
    const applyDark = () => {
      root.classList.add("dark");
      document.body.classList.remove("light-theme","bg-[#f8f4f0]");
      document.body.classList.add("bg-gradient-to-br","from-indigo-600","via-indigo-700","to-violet-700");
    };

    if (saved === "light") { toggle.checked = true; applyLight(); }
    else { applyDark(); }

    toggle.addEventListener("change", () => {
      if (toggle.checked) { applyLight(); localStorage.setItem("theme","light"); }
      else { applyDark(); localStorage.setItem("theme","dark"); }
    });
  },
  methods: {
    showNotification(msg, type="info") {
      this.notification = { show: true, message: msg, type };
      setTimeout(() => { this.notification.show = false; }, 3000);
    },

    goToList() { this.mode = 'list'; },
    goToForm() { this.mode = 'form'; },

    async fetchUsers() {
      if (this.search.length < 2) { this.suggestions = []; return; }
      try {
        const res = await axios.get(`/ldap/search?term=${this.search}`);
        this.suggestions = res.data.slice(0, 3);
        this.showSuggestions = true;
      } catch (e) { console.error('Fetch users error:', e); }
    },
    selectUser(user) {
      this.search = user.username;
      this.selectedUser = user;
      this.suggestions = [];
      this.showSuggestions = false;
    },
    applySuggestion() {
      if (!this.selectedUser || this.search !== this.selectedUser.username) {
        this.selectedUser = null;
      }
      this.showSuggestions = false;
    },

    formatAssetTag(input) {
      let raw = String(input).trim().toUpperCase();
      if (raw.startsWith("ST")) raw = raw.slice(2);
      raw = raw.replace(/\D/g, "");
      if (raw.length === 0 || raw.length > 4) return null;
      return "ST" + raw.padStart(4, "0");
    },
    ownersForTag(tag, excludeUser) {
      const owners = this.vinculos
        .filter(v => v.asset_tag === tag && v.username !== excludeUser)
        .map(v => v.username);
      return [...new Set(owners)];
    },

    addVinculo() {
      if (!this.selectedUser || !this.assetNumber) {
        this.showNotification("Selecione um usuário válido e insira o número do ativo.", "error");
        return;
      }

      const tag = this.formatAssetTag(this.assetNumber);
      if (!tag) { 
        this.showNotification("Número do ativo inválido. Use 1 a 4 dígitos.", "error");
        return;
      }

      const owners = this.ownersForTag(tag, this.selectedUser.username);
      if (owners.length > 0) {
        this.confirmDuplicate(tag, owners);
        return;
      }

      this.vinculos.push({ username: this.selectedUser.username, asset_tag: tag, duplicate: false });
      this.search = '';
      this.selectedUser = null;
      this.assetNumber = '';
      this.suggestions = [];
    },

    confirmDuplicate(tag, owners) {
      this.duplicatePrompt = { show: true, tag, user: this.selectedUser.username, owners };
    },
    acceptDuplicate() {
      this.vinculos.push({ username: this.selectedUser.username, asset_tag: this.duplicatePrompt.tag, duplicate: true });
      this.duplicatePrompt = { show: false, tag: '', user: '', owners: [] };
      this.search = '';
      this.selectedUser = null;
      this.assetNumber = '';
      this.suggestions = [];
      this.showNotification("Duplicado cadastrado!", "warn");
    },
    cancelDuplicate() {
      this.duplicatePrompt = { show: false, tag: '', user: '', owners: [] };
      this.showNotification("Cadastro cancelado.", "info");
    },

    editVinculo(index) {
      this.editIndex = index;
      this.editUsername = this.vinculos[index].username;
      this.editAsset = this.vinculos[index].asset_tag;
    },
    salvarEdicao() {
      if (this.editIndex !== null) {
        this.vinculos[this.editIndex].username = this.editUsername;
        this.vinculos[this.editIndex].asset_tag = this.editAsset;
        this.editIndex = null;
        this.editUsername = '';
        this.editAsset = '';
        this.showNotification("Vínculo atualizado!", "success");
      }
    },
    cancelarEdicao() {
      this.editIndex = null;
      this.editUsername = '';
      this.editAsset = '';
    },

    async enviarVinculos() {
      if (this.vinculos.length === 0) { 
        this.showNotification("Nenhum vínculo para enviar.", "error"); 
        return; 
      }
      try {
        const payload = this.vinculos.map(v => ({ username: v.username, asset_tag: v.asset_tag }));
        await axios.post("/assign/vincular-ativos", payload, { headers: { "Content-Type": "application/json" } });
        this.showNotification("Vínculos enviados com sucesso!", "success");
        this.vinculos = [];
      } catch (e) {
        console.error("Send vinculos error:", e);
        this.showNotification("Erro ao enviar vínculos.", "error");
      }
    },

    async baixarCSV() {
      if (this.vinculos.length === 0) { 
        this.showNotification("Nenhum vínculo para exportar.", "error"); 
        return; 
      }
      try {
        const header = "username,asset_tag,duplicado\n";
        const rows = this.vinculos.map(v => {
          return `${v.username},${v.asset_tag},${v.duplicate ? "#duplicated" : ""}`;
        }).join("\n");
      
        const csv = header + rows;
      
        const blob = new Blob([csv], { type: "text/csv" });
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "transferencias.csv";
        document.body.appendChild(link);
        link.click();
        link.remove();
      
        this.showNotification("CSV baixado com sucesso!", "success");
      } catch (e) {
        console.error("Download CSV error:", e);
        this.showNotification("Erro ao baixar CSV.", "error");
      }
    }
  }
}).mount("#app");