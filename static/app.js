import home from './components/home.js'
import login from './components/login.js'
import signup from './components/signup.js'
import bookings from './components/bookings.js'
import user_dashboard from './components/user_dashboard.js'
import admin_dashboard from './components/admin_dashboard.js'



const router = new VueRouter({
    routes: [
        {path: '/', component: home },
        {path: '/bookings', component: bookings },
        {path: '/signup', component: signup},
        {path: '/login', component: login },
        {path: '/user_dashboard', component: user_dashboard},
        {path: '/admin_dashboard', component: admin_dashboard}
    ],
})


new Vue({
    el: '#app',
    delimiters: ['${','}'],
    router,
})