// user-dashboard.js
export default {
  template: `
    <div>
      <h1>User Dashboard</h1>
      <p>Welcome to the user dashboard! check your bookings here <a ><router-link to="/bookings">My Bookings</router-link></a></p>
      <hr>
      <h2> Shows to enjoy this weekend!! </h2>
      <hr>
      <label for="filter-input"><b>Search for your venue: </b></label>
      <input type="text" v-model="filter" placeholder="Venue">
      <br><br>
      <div v-for="hall in filtered_halls">

        <h2><b>Venue: </b>{{ hall.place }}</h2>
        <p><b>Hall: </b>{{ hall.hall_name }} <i> // </i>  <b>Capacity: </b>{{ hall.size }}</p>

        <div v-for="show in hall.shows">
          <h5><b>Show ID: </b>{{ show.show_id }}</h5>
          <p><b>Show Name: </b>{{ show.show_name }}<b> About: </b>{{ show.about }}<b> Genre: </b>{{ show.genre }}<b> Rating: </b>{{ show.rating }}</p>
          <p><b> Time: </b>{{ show.time }}<b> Ticket lefts: </b>{{ show.left_seat }}<b> Price: </b>{{ show.ticketPrice }}</p>
          <button @click="showBookingForm(show)">Book Tickets</button>
        </div>
        <hr>

        <div v-if="showBooking">
        <h4>{{selectedShow.name}}</h4>

          <form @submit.prevent="bookTicket">

            <label>
              Number of tickets:
              <input v-model="bookingData.n_tickets" type="number">
            </label>

            <button>Book Now</button>

          </form>

        </div>

      </div>
    </div>
  `,
  data(){
    return{
      filter: '',
      halls: [],
      filtered_halls: [],
      bookingData: {
        n_tickets: null
      },
      showBooking: false,
      bookings: [],
      user: null,
      selectedShow: null 
    }
  },
  watch: {
    filter(newFilter) {
      if (!newFilter) {
        this.filtered_halls=this.halls 
      } else {
        this.filtered_halls=this.halls.filter(hall => hall.place.toLowerCase().includes(newFilter.toLowerCase()))
      }
    },
  },
  created(){
    this.fetchHalls()
  },
  methods: {
    fetchHalls() {
    
      fetch('/api/hall')
        .then(res => res.json())
        .then(halls => {
  
          const promises = halls.map(hall => {
            return fetch(`/api/show/${hall.hall_id}`)
              .then(res => res.json())
              .then(shows => {
                hall.shows = shows;
                console.log(hall)
                return hall;
              });
          })
          
          return Promise.all(promises);
  
        })
        .then(halls => {
          this.halls = halls; 
          this.filtered_halls = halls
        })
        .catch(err => {
          console.error('Error fetching halls', err);
        });
  
    },
    showBookingForm(show){
      this.selectedShow=show
      this.showBooking=true 
    },
    bookTicket() {
      const show = this.selectedShow;
      fetch('/api/user')
        .then(res => res.json())
        .then((data) => {
  
          const user_id = data.response.user_id

          const bookingData = {
            n_tickets: this.bookingData.n_tickets,
          };
  
          return fetch(`/api/booking/${user_id}/${show.hall_id}/${show.show_id}`, {
            method: 'POST', 
            headers: {
              'Content-Type': 'application/json'  
            },
            body: JSON.stringify(bookingData) 
          })
        
        })
        .then(res => res.json())
        .then(booking => {
          this.bookings.push(booking)
          this.bookingData = {}
          this.showBooking = false
          this.fetchHalls()
          this.filter=''
        
        })
        .catch(err => {
           console.log('Error booking ticket', err)
        });
    },
  }
}
  