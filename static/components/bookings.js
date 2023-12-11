export default {
    template: `
    <div> 
    <h1> Find Your Booking history </h1><hr>
        <div v-for="booking in bookings">
            <h3><b>Booking ID: </b>{{ booking.booking_id }}</h3>
            <h4><b>Date and Time: </b>{{ booking.time }}</h4>
            <p><b>Venue: </b>{{ booking.place }}<b> Show Name: </b>{{ booking.show_name }}<b> Nuber of tickets: </b>{{ booking.n_tickets }}<b> Total Cost: </b>{{ booking.total_price }}</p>
            <button @click="deleteBooking(booking)">Delete This Booking History</button><br>
            <hr>
        </div>
    </div>
    `,
    data(){
        return{
            bookings: [],
        }
    },
    created(){
        this.fetchBookings()
    },
    methods:{
        fetchBookings(){
            let user_id
            fetch('/api/user')
                .then(res => res.json())
                .then((data) => {
                    user_id=data.response.user_id
                    return fetch(`/api/booking/${user_id}`)
                })
                .then(bookRes => bookRes.json())
                .then(bookData => {
                    console.log(bookData)
                    this.bookings = bookData 
                })
                .catch((error) => {
                    console.error('Error fetching bookings:', error);
                })
        },
        deleteBooking(booking){
            fetch('/api/user')
                .then((response) => response.json())
                .then((data) => {
                    const user_id = data.response.user_id
                    return fetch(`/api/booking/${user_id}/${booking.hall_id}/${booking.show_id}/${booking.booking_id}`,{
                    method: 'DELETE'
                    })
                })
                .catch((error) => {
                    console.error('Error deleting booking:', error)
                })
                this.fetchBookings()
            }
    }
}