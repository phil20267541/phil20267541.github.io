  const app = Vue.createApp({
    data() {
        content = [
            { title: 'CV', description: 'My CV', link: 'https://phil20267541.github.io/CV_Website/', image: 'Resources/cv.png' },
            { title: 'Shoop', description: 'All hail the shoop', link: 'https://phil20267541.github.io/Shoop/', image: 'Resources/shoop.png' }
        ]
        projects = [{title:'CV', link: '#cv'}, {title:'Shoop', link: '#shoop'}]
      return {
        content, projects
      }
    }
  })

 app.mount('#app')