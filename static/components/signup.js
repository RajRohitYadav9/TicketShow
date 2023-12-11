export default {
    template: `
      <div>
        <h1>Signup</h1>
        <form @submit.prevent="onSubmit">
          <input placeholder="username" type="text" v-model="username" />
          <br />
          <input placeholder="email" type="email" v-model="email" />
          <br />
          <input placeholder="password" type="password" v-model="password" />
          <br />
          <input placeholder="roles" type="password" v-model="roles" />
          <br />
          <button type="submit">Submit</button>
        </form>
        <p v-if="message">{{ message }}</p>
      </div>
    `,
    data() {
      return {
        username: '',
        email: '',
        password: '',
        roles: '',
        message: ''
      }
    },
    methods: {
      async onSubmit() {
        const response = await fetch('/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
            roles: this.roles
          })
        });
        
        if (response.ok) {
          this.message = 'Signup successful!';
        } else {
          this.message = 'Signup failed. Please try again.';
        }
      }
    }
  }