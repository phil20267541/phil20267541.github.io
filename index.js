const app = Vue.createApp({
  data() {
    return {
      content: [],
      projects: [],
      success: false
    };
  },
  methods: {
    async fetchData() {
      try {
        const res = await fetch('https://phil20267541-hompage-backend.onrender.com/api/index/data');
        const data = await res.json();
        this.content = data.content;
        this.projects = data.projects;
        this.success = data.success;
      } catch (err) {
        console.error('Error fetching data:', err);
      }
    }
  },
  mounted() {
    // Runs when the Vue app is first loaded
    this.fetchData();
  }
});

app.mount('#app');