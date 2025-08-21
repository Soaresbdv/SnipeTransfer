const { createApp } = Vue

createApp({
  data() {
    return {
      search: '',
      assetNumber: '',
      suggestions: [],
      vinculos: []
    }
  },
  methods: {
    fetchUsers() {
      if (this.search.length < 3) return
      axios.get(`/ldap/search?term=${this.search}`)
        .then(res => {
          this.suggestions = res.data
        })
    },
    addVinculo() {
      if (!this.search || !this.assetNumber) return
      const asset_tag = `ST${String(this.assetNumber).padStart(4, '0')}`
      this.vinculos.push({ username: this.search.toLowerCase(), asset_tag })
      this.assetNumber = ''
    },
    enviarVinculos() {
      axios.post('/assign/vincular-ativos', this.vinculos)
        .then(() => {
          alert("Vínculos enviados com sucesso!")
        })
    },
    baixarCSV() {
      window.open('/assign/exportar-ativos', '_blank')
    }
  }
}).mount('#app')