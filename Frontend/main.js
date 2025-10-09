const app = Vue.createApp({
  data() {
    return {
      content: [],
      projects: []
    };
  },
  methods: {
    async fetchData() {
      try {
        const res = await fetch('https://your-flask-app.onrender.com/api/data');
        const data = await res.json();
        this.content = data.content;
        this.projects = data.projects;
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