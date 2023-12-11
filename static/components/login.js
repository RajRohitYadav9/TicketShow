export default {
    template: `<div>Login Form
    <input type='email' placeholder='email' v-model='credential.email' />
    <input type='password' placeholder='password' v-model='credential.password' />
    <button @click='loginUser'> Login </button>
    </div>`,

    data(){
        return {
            credential: {
                email: null,
                password: null,
            }, 
        }
    },
    methods: {
        loginUser(){
            fetch('/login?include_auth_token', {
                method: 'POST',
                body: JSON.stringify(this.credential),
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res)=> {
                return res.json()
            }).then((data)=>{
                console.log(data.response.user.authentication_token)
                localStorage.setItem('authToken', data.response.user.authentication_token)

                this.fetchUserData()
            }).catch((error) => {
                console.error('Login error:', error)
            })

        },
        fetchUserData(){
            const authToken=localStorage.getItem('authToken')
            fetch('/api/user',{
                headers:{
                    Authorisation: `Bearer ${authToken}`,
                },
            })
            .then((res) => res.json())
            .then((data) => {
                const userRoles = data.response.roles 
                if (userRoles.includes('admin')){
                    this.$router.push('/admin_dashboard')
                } else {
                    this.$router.push('/user_dashboard')
                }
            })
            .catch((error) => {
                console.error('Error fetching user data:', error)
            })

        },
    },
}