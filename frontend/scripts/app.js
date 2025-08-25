const { createApp } = Vue;

createApp({
  data() {
    return {
      search: '',
      suggestions: [],
      selectedUser: null,
      showSuggestions: false,
      assetNumber: '',
      vinculos: []
    };
  },
  methods: {
    async fetchUsers() {
      if (this.search.length < 2) {
        this.suggestions = [];
        return;
      }

      try {
        const response = await axios.get(`/ldap/search?term=${this.search}`);
        this.suggestions = response.data;
        this.showSuggestions = true;
      } catch (error) {
        console.error('Erro ao buscar usuários:', error);
      }
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

    addVinculo() {
      if (!this.selectedUser || !this.assetNumber) {
        alert("Selecione um usuário válido e insira o número do ativo.");
        return;
      }
    
      this.vinculos.push({
        username: this.selectedUser.username,
        asset_tag: String(this.assetNumber)
      });
    
      this.search = '';
      this.selectedUser = null;
      this.assetNumber = '';
      this.suggestions = [];
    },

    async enviarVinculos() {
      if (this.vinculos.length === 0) {
        alert("Nenhum vínculo para enviar.");
        return;
      }
    
      try {
        await axios.post("/assign/vincular-ativos", this.vinculos, {
          headers: { "Content-Type": "application/json" }
        });
        alert("Vínculos enviados com sucesso!");
        this.vinculos = [];
      } catch (error) {
        console.error("Erro ao enviar vínculos:", error);
        alert("Erro ao enviar vínculos.");
      }
    },

    async baixarCSV() {
      if (this.vinculos.length === 0) {
        alert("Nenhum vínculo para exportar.");
        return;
      }

      try {
        await axios.post("/assign/vincular-ativos", this.vinculos, {
          headers: { "Content-Type": "application/json" }
        });
        this.vinculos = [];

        const url = `/assign/exportar-ativos?t=${Date.now()}`;
        const response = await axios.get(url, {
          responseType: "blob",
          headers: { "Cache-Control": "no-cache" }
        });

        const blob = new Blob([response.data], { type: "text/csv" });
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "vinculos.csv";
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error("Erro ao baixar CSV:", error);
        alert("Erro ao baixar CSV.");
      }
    },
  },
}).mount("#app");