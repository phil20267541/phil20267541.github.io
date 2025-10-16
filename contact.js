const app = Vue.createApp({
  data() {
    return {
      name: '',
      email: '',
      message: '',
      errors: {},
      submitted: false,
      success_name: '',
      success_email: '',
      success_message: '',
      success: false
    };
  },
  methods: {
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },

    submitForm() {
      this.errors = {};
      this.submitted = false;

      // Name validation
      if (!this.name) {
        this.errors.name = "Name is required.";
      }

      // Email validation
      if (!this.email) {
        this.errors.email = "Email is required.";
      } else if (!this.validateEmail(this.email)) {
        this.errors.email = "Email is not valid.";
      }

      // Message validation
      if (!this.message) {
        this.errors.message = "Message is required.";
      }

      // If no errors, submit form
      if (Object.keys(this.errors).length === 0) {
        this.sendData();
      }
    },

    async sendData() {
      try {
        const res = await fetch('https://phil20267541-hompage-backend.onrender.com/api/contact/submit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            message: this.message
          })
        });
        const result = await res.json();

          if (res.ok) {
            this.submitted = true;
            this.success_name = this.name
            this.success_email = this.email
            this.success_message = this.message
            this.success = true
            this.name = '';
            this.email = '';
            this.message = '';
          } else {
            if (result.errors) {
              this.errors = result.errors;
            } else if (result.error) {
              console.error(result.error);
            }
          }
        } catch (err) {
          console.error('Error submitting form:', err);
      }
    }
  },
});

app.mount('#app');