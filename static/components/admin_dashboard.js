// admin-dashboard.js
export default {
    template: `
    <div>
      <h1> Welcome to Admin's Dashboard </h1>
      <hr>
      <h3>Theaters and Shows this weekend:</h3>
      <br>
      <div>

      <!-- Display Halls -->

      <div v-for="hall in halls">

        <!-- Edit Hall Form -->
        <div v-if="editHallForm.hall_id == hall.hall_id">  
          <input v-model="editHallForm.hall_name">
          <input v-model="editHallForm.place">
          <input v-model="editHallForm.size">
          <button @click="editHallSave">Save Hall</button>
        </div>

        <p><b>Venue: </b>{{ hall.place }}<b> ID: </b>{{ hall.hall_id }}</p>
        <p><b>Hall: </b>{{ hall.hall_name }}</p>
        <p><b>Capacity: </b>{{ hall.size }}</p>
        
        <button @click="editHall(hall)">Edit Hall</button>
        <button @click="deleteHall(hall)">Delete Hall</button><br>

        <!-- Shows for this hall -->

        <div v-for="show in hall.shows">
        
          <h4><b>Show Name: </b>{{ show.show_name }}<b> Date & Time: </b>{{ show.time }}</h4>
          <p><b>About: </b>{{ show.about }}<b> Genre: </b>{{ show.genre }}<b> Rating: </b>{{ show.rating }}<b> Left seat: </b>{{ show.left_seat }}<b> Ticket Price: </b>{{ show.ticketPrice }}</p>
          
          
          <button @click="editShow(show)">Edit Show</button>
          <button @click="deleteShow(show)">Delete Show</button>
        
        </div><br>

        <!-- New Show Form -->
        <input v-model="newShow.hall_id" placeholder="hall_id" type="number">
        <input v-model="newShow.show_name" placeholder="show_name" type="text">
        <input v-model="newShow.about" placeholder="about" type="text">
        <input v-model="newShow.genre" placeholder="genre" type="text">
        <input v-model="newShow.rating" placeholder="rating" type="number">
        <input v-model="newShow.time" placeholder="time" type="text">
        <input v-model="newShow.ticketPrice" placeholder="ticketPrice" type="number">
        <button @click="createShow">Create Show</button>
        <br>
        <div v-if="editShowForm.show_id !== show.show_id">
          <input v-model="editShowForm.show_name" placeholder="show_name" type="text">
          <input v-model="editShowForm.about" placeholder="about" type="text">
          <input v-model="editShowForm.genre" placeholder="genre" type="text">
          <input v-model="editShowForm.rating" placeholder="rating" type="number">
          <input v-model="editShowForm.time" placeholder="time" type="text">
          <input v-model="editShowForm.ticketPrice" placeholder="ticketPrice" type="number">
          <button @click="editShowSave">Save Show</button>
        </div>
        <hr>
      </div><hr>

      <!-- New Hall Form -->
      <h3>Create New Hall</h3>
      <input v-model="newHall.hall_name" placeholder="hall_name" type="text">
      <input v-model="newHall.place" placeholder="Venue" type="text">
      <input v-model="newHall.size" placeholder="Capacity" type="number">

      <button @click="createHall">Create Hall</button>
  
      </div><hr>
      <button type="button" v-on:click="export_halls">Export your halls with shows</button>
      <hr>
    </div>
    `,
    data() {
      return {
        newHall: {
          hall_name: "",
          place: "",
          size: null,
        },
        halls: [],
        editHallForm: {
          hall_id: null,
          hall_name: '',
          place: '',
          size: null,
        },
        show: {
          show_id: null,
          show_name: '',
          about: '',
          genre: '',
          rating: 0,
          time: '',
          ticketPrice: 0,
        },
        newShow: {
          hall_id: null,
          show_name: "",
          about: "",
          genre: "",
          rating: null,
          time: "",
          ticketPrice: null,
        },
        editShowForm: {
          hall_id: null,
          show_id: null,
          show_name: "",
          about: "",
          genre: "",
          rating: null,
          time: "",
          ticketPrice: null,
        },
      }
    },
    created() {
      this.fetchHalls()
    },
    methods: {
      fetchHalls() {
        let user_id;
      
        fetch('/api/user') 
          .then(res => res.json())
          .then(data => {
            user_id = data.response.user_id;
      
            return fetch(`/api/hall/${user_id}`);
      
          })
          .then(hallRes => hallRes.json())
          .then(hallData => {
            const hallPromises = hallData.map(hall => {
      
              return fetch(`/api/shows/${user_id}/${hall.hall_id}`)
                .then(showRes => showRes.json())
                .catch(err => {
                  console.log('No shows found for hall', hall.hall_id);
                  return [];  
                })
                .then(shows => {
                  hall.shows = shows;
                  console.log(hall)
                  return hall;
                });
      
            });
            
            return Promise.all(hallPromises);
            
          })
          .then(halls => {
            this.halls = halls;
          })
          .catch(err => {
            console.error('Error fetching halls', err);
          });
      
      },
      createHall() {
        fetch('/api/user')
          .then((response) => response.json())
          .then((data) => {
            const user_id = data.response.user_id
            return fetch(`/api/hall/${user_id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(this.newHall),
            })
          })
          .then((response) => response.json())
          .then((data) => {
            this.halls.push(data)
            this.newHall={
              hall_name: '',
              place: '',
              size: null,
            }
          })
          .catch((error) => {
            console.error('Error creating Hall:', error);
          })
      },
      editHall(hall) {
        this.editHallForm.hall_id = hall.hall_id;
        this.editHallForm.hall_name = hall.hall_name;
        this.editHallForm.place = hall.place;
        this.editHallForm.size = hall.size;
      },
      editHallSave() {
        fetch('/api/user')
          .then((response) => response.json())
          .then((data) => {
            const user_id = data.response.user_id;
            return fetch(`/api/hall/${user_id}/${this.editHallForm.hall_id}`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(this.editHallForm),
            });
          })
          .then(() => {
            const index = this.halls.findIndex((hall) => hall.hall_id === this.editHallForm.hall_id);
            if (index !== -1) {
              this.halls[index] = this.editHallForm;
            }
            this.editHallForm = {
              hall_id: null,
              hall_name: '',
              place: '',
              size: null,
            };
          })
          .catch((error) => {
            console.error('Error updating Hall:', error)
          });
      },
      deleteHall(hall){
        fetch('/api/user')
          .then((response) => response.json())
          .then((data) => {
            const user_id = data.response.user_id
            return fetch(`/api/hall/${user_id}/${hall.hall_id}`, {
              method: 'DELETE'
            })
          })
          .then(() => {
            const index = this.halls.findIndex((h) => h.hall_id === hall.hall_id);
            if (index !== -1) {
              this.halls.splice(index, 1);
          }
          })
          .catch((error) => {
            console.error('Error deleting Hall:', error)
          })
      },
      createShow() {
        fetch('/api/user')
          .then((response) => response.json())
          .then((data) => {
            const user_id = data.response.user_id;
            return fetch(`/api/shows/${user_id}/${this.newShow.hall_id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(this.newShow),
            });
          })
          .then((response) => {
            if (response.status === 201) {
              return response.json();
            } else {
              throw new Error('Failed to create show');
            }
          })
          .then((data) => {
            this.fetchHalls();
    
            
            this.newShow = {
              hall_id: null,
              show_name: '',
              about: '',
              genre: '',
              rating: null,
              time: '',
              ticketPrice: null,
            };
          })
          .catch((error) => {
            console.error('Error creating Show:', error);
          });
      },
      editShow(show) {
        this.editShowForm.hall_id = show.hall_id;
        this.editShowForm.show_id = show.show_id;
        this.editShowForm.show_name = show.show_name;
        this.editShowForm.about = show.about;
        this.editShowForm.genre = show.genre;
        this.editShowForm.rating = show.rating;
        this.editShowForm.time = show.time;
        // this.editShowForm.left_seat = show.left_seat;
        this.editShowForm.ticketPrice = show.ticketPrice;
      },
      editShowSave() {
        fetch('/api/user')
          .then((response) => response.json())
          .then((data) => {
            const user_id = data.response.user_id;
            return fetch(`/api/shows/${user_id}/${this.editShowForm.hall_id}/${this.editShowForm.show_id}`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(this.editShowForm),
            });
          })
          .then((response) => {
            if (response.status === 200) {
              this.fetchHalls(); 
              this.editShowForm = {
                hall_id: null,
                show_id: null,
                show_name: '',
                about: '',
                genre: '',
                rating: null,
                time: '',
                // left_seat: null,
                ticketPrice: null,
              };
            } else {
              throw new Error('Failed to update show');
            }
          })
          .catch((error) => {
            console.error('Error updating Show:', error);
          });
      },
      deleteShow(show) {
        fetch('/api/user')
          .then((response) => response.json())
          .then((data) => {
            const user_id = data.response.user_id;
            return fetch(`/api/shows/${user_id}/${show.hall_id}/${show.show_id}`, {
              method: 'DELETE',
            });
          })
          .then((response) => {
            if (response.status === 200) {
              this.fetchHalls(); 
            } else {
              throw new Error('Failed to delete show');
            }
          })
          .catch((error) => {
            console.error('Error deleting Show:', error);
          });
      },
      export_halls: function () {
        window.open('/export_halls', '_blank').focus();
      }
    }
}