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
      vinculos: []
    };
  },
  mounted() {
    const toggle = document.getElementById("theme-toggle");
    const root = document.documentElement;
    const saved = localStorage.getItem("theme");

    if (saved === "light") {
      toggle.checked = true;
      root.classList.remove("dark");
      document.body.classList.add("light-theme");
    } else {
      root.classList.add("dark");
    }

    toggle.addEventListener("change", () => {
      if (toggle.checked) {
        root.classList.remove("dark");
        document.body.classList.add("light-theme");
        localStorage.setItem("theme", "light");
      } else {
        root.classList.add("dark");
        document.body.classList.remove("light-theme");
        localStorage.setItem("theme", "dark");
      }
    });
  },
  methods: {
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
        alert("Selecione um usuário válido e insira o número do ativo.");
        return;
      }

      const tag = this.formatAssetTag(this.assetNumber);
      if (!tag) { alert("Número do ativo inválido. Use 1 a 4 dígitos."); return; }

      const owners = this.ownersForTag(tag, this.selectedUser.username);
      if (owners.length > 0) {
        const proceed = confirm(
          `O ativo ${tag} já está na lista com: ${owners.join(", ")}.\nDeseja inserir mesmo assim?`
        );
        if (!proceed) return;
      }

      this.vinculos.push({ username: this.selectedUser.username, asset_tag: tag });
      this.search = '';
      this.selectedUser = null;
      this.assetNumber = '';
      this.suggestions = [];
    },

    async enviarVinculos() {
      if (this.vinculos.length === 0) { alert("Nenhum vínculo para enviar."); return; }
      try {
        const payload = this.vinculos.map(v => ({ username: v.username, asset_tag: v.asset_tag }));
        await axios.post("/assign/vincular-ativos", payload, { headers: { "Content-Type": "application/json" } });
        alert("Vínculos enviados com sucesso!");
        this.vinculos = [];
      } catch (e) {
        console.error("Send vinculos error:", e);
        alert("Erro ao enviar vínculos.");
      }
    },

    async baixarCSV() {
      if (this.vinculos.length === 0) { alert("Nenhum vínculo para exportar."); return; }
      try {
        const payload = this.vinculos.map(v => ({ username: v.username, asset_tag: v.asset_tag }));
        await axios.post("/assign/vincular-ativos", payload, { headers: { "Content-Type": "application/json" } });
        this.vinculos = [];

        const url = `/assign/exportar-ativos?t=${Date.now()}`;
        const response = await axios.get(url, {
          responseType: "blob",
          headers: { "Cache-Control": "no-cache" }
        });

        const blob = new Blob([response.data], { type: "text/csv" });
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "transferencias.csv";
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (e) {
        console.error("Download CSV error:", e);
        alert("Erro ao baixar CSV.");
      }
    }
  }
}).mount("#app");