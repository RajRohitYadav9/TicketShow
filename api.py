from flask_restful import Resource, reqparse, fields, marshal_with
from error import NotFoundError, UserManagementError, HallManagementError, ShowsManagementError, BookingsManagementError
from models import User, db, Hall, Shows, Bookings
from sec import store
# from flask_security import hash_password
from flask_security.decorators import auth_required
from flask_login import login_required







# API for managing new registeration.

register_fields = {
   'username': fields.String,
   'email': fields.String,
   'password': fields.String,
   'roles': fields.String
}

# Request parser for parsing JSON data in requests
register_user_parser=reqparse.RequestParser()
register_user_parser.add_argument('username')
register_user_parser.add_argument('email')
register_user_parser.add_argument('password')
register_user_parser.add_argument('roles')





class registerAPI(Resource):
   @marshal_with(register_fields)
   def post(self):
      args = register_user_parser.parse_args()
      username=args.get("username", None)
      email=args.get("email", None)
      password=args.get("password", None)
      roles=args.get("roles", None)
    
      if username is None:
         raise UserManagementError(status_code=400, error_code="UM1001", error_message="username is required")
      if email is None:
         raise UserManagementError(status_code=400, error_code="UM1002", error_message="email is required")
      if password is None:
         raise UserManagementError(status_code=400, error_code="UM1003", error_message="password is required")
      if roles is None:
         raise UserManagementError(status_code=400, error_code="UM1004", error_message="roles is required")
    
      if not store.find_user(email=email):
         store.create_user(email=email, password=password, username=username, roles=[roles])
      db.session.commit()
      return 201
    



# API for managing Hall.

hall_fields = {
   'user_id': fields.Integer,
   'hall_id': fields.Integer,
   'hall_name': fields.String,
   'place': fields.String,
   'size': fields.Integer
}

# Request parser for parsing JSON data in requests
create_hall_parser=reqparse.RequestParser()
create_hall_parser.add_argument('hall_name')
create_hall_parser.add_argument('place')
create_hall_parser.add_argument('size')


update_hall_parser=reqparse.RequestParser()
update_hall_parser.add_argument('hall_name')
update_hall_parser.add_argument('place')
update_hall_parser.add_argument('size')




class HallManagerAPI(Resource):
   @marshal_with(hall_fields)
   @login_required
   def get(self, user_id):
      hall = Hall.query.filter_by(user_id=user_id).all()
      print(hall)
      if hall:
         return hall
      return NotFoundError(status_code=404)

   @marshal_with(hall_fields)
   @login_required
   def post(self, user_id):
      args = create_hall_parser.parse_args()
      hall_name=args.get("hall_name", None)
      place=args.get("place", None)
      size=args.get("size", None)
    
      if hall_name is None:
         raise HallManagementError(status_code=400, error_code="HM1001", error_message="hall_name is required")
      if place is None:
         raise HallManagementError(status_code=400, error_code="HM1002", error_message="place is required")
      if size is None:
         raise HallManagementError(status_code=400, error_code="HM1003", error_message="size is required")
    
      new_hall=Hall(user_id=user_id, hall_name=hall_name, place=place, size=size)
      db.session.add(new_hall)
      db.session.commit()
      return new_hall, 201

   @marshal_with(hall_fields)
   @login_required
   def put(self, user_id, hall_id):
      args=update_hall_parser.parse_args()
      hall_name=args.get("hall_name", None)
      place=args.get("place", None)
      size=args.get("size", None)
      hall = Hall.query.get(hall_id)
    
      if hall_name is None:
         raise HallManagementError(status_code=400, error_code="HM1001", error_message="hall_name is required")
      if place is None:
         raise HallManagementError(status_code=400, error_code="HM1002", error_message="place is required")
      if size is None:
         raise HallManagementError(status_code=400, error_code="HM1003", error_message="size is required")

      hall = Hall.query.filter_by(user_id=user_id, hall_id=hall_id).first()
      if hall:
         hall.hall_name=hall_name
         hall.place=place 
         hall.size=size 
         db.session.add(hall)
         db.session.commit()
         return hall 
      else:
         raise NotFoundError(status_code=404)

   @login_required
   def delete(self, user_id, hall_id):
      hall = Hall.query.filter_by(user_id=user_id, hall_id=hall_id).first()
      if hall:
         db.session.delete(hall)
         db.session.commit()  
         return "", 200
      else:
         raise  NotFoundError(status_code=404)



# API  for managing shows

Show_fields={
  "user_id" : fields.Integer,
  "hall_id" : fields.Integer,
  "show_id" : fields.Integer,
  "show_name" : fields.String,
  "about" : fields.String,
  "genre" : fields.String,
  "rating" : fields.Float,
  "time" : fields.String,
  "left_seat" : fields.Integer,
  "ticketPrice" : fields.Integer,
}


update_show_parser=reqparse.RequestParser()
update_show_parser.add_argument('show_name')
update_show_parser.add_argument('about')
update_show_parser.add_argument('genre')
update_show_parser.add_argument('rating')
update_show_parser.add_argument('time')
update_show_parser.add_argument('left_seat')
update_show_parser.add_argument('ticketPrice')


create_show_parser=reqparse.RequestParser()
create_show_parser.add_argument('show_name')
create_show_parser.add_argument('about')
create_show_parser.add_argument('genre')
create_show_parser.add_argument('rating')
create_show_parser.add_argument('time')
create_show_parser.add_argument('left_seat')
create_show_parser.add_argument('ticketPrice')


class ShowManagerAPI(Resource):
   @marshal_with(Show_fields)
   @login_required
   def get(self, user_id, hall_id):
      show = Shows.query.filter_by(user_id=user_id, hall_id=hall_id).all()
      if show:
         return show 
      else:
         raise  NotFoundError(status_code=404)
    

   @marshal_with(Show_fields)
   @login_required
   def put(self, user_id, hall_id, show_id):
      args=update_show_parser.parse_args()
      show_name=args.get("show_name", None)
      about=args.get("about", None)
      genre=args.get("genre", None)
      rating=args.get("rating", None)
      time=args.get("time", None)
      ticketPrice=args.get("ticketPrice", None)

      if show_name is None:
         raise ShowsManagementError(status_code=400, error_code="SM1001", error_message="show_name is required")
      if about is None:
         raise ShowsManagementError(status_code=400, error_code="SM1002", error_message="about is required")
      if genre is None:
         raise ShowsManagementError(status_code=400, error_code="SM1003", error_message="genre is required")
      if rating is None:
         raise ShowsManagementError(status_code=400, error_code="SM1004", error_message="rating is required")
      if time is None:
         raise ShowsManagementError(status_code=400, error_code="SM1005", error_message="time is required")
      if ticketPrice is None:
         raise ShowsManagementError(status_code=400, error_code="SM1006", error_message="ticketPrice is required")
    
      hall=Hall.query.filter_by(user_id=user_id, hall_id=hall_id).first()
      show=Shows.query.filter_by(user_id=user_id, hall_id=hall_id, show_id=show_id).first()
      if show:
         show.show_name=show_name
         show.about=about
         show.genre=genre
         show.rating=rating
         show.time=time
         show.left_seat=hall.size
         show.ticketPrice=ticketPrice

         db.session.add(show)
         db.session.commit()
         return show
      else:
         raise NotFoundError(status_code=404)
    
   @login_required
   def delete(self, user_id, hall_id, show_id):
      show=Shows.query.filter_by(user_id=user_id, hall_id=hall_id, show_id=show_id).first()
      if show:
         db.session.delete(show)
         db.session.commit()
         return "", 200
      else:
         raise NotFoundError(status_code=404)

   @login_required 
   def post(self, user_id, hall_id):
      args=create_show_parser.parse_args()
      show_name=args.get("show_name", None)
      about=args.get("about", None)
      genre=args.get("genre", None)
      rating=args.get("rating", None)
      time=args.get("time", None)
      ticketPrice=args.get("ticketPrice", None)

      if show_name is None:
         raise ShowsManagementError(status_code=400, error_code="SM1001", error_message="show_name is required")
      if about is None:
         raise ShowsManagementError(status_code=400, error_code="SM1002", error_message="about is required")
      if genre is None:
         raise ShowsManagementError(status_code=400, error_code="SM1003", error_message="genre is required")
      if rating is None:
         raise ShowsManagementError(status_code=400, error_code="SM1004", error_message="rating is required")
      if time is None:
         raise ShowsManagementError(status_code=400, error_code="SM1005", error_message="time is required")
      if ticketPrice is None:
         raise ShowsManagementError(status_code=400, error_code="SM1006", error_message="ticketPrice is required")
    
      hall=Hall.query.filter_by(user_id=user_id, hall_id=hall_id).first()
      if hall:
         new_show=Shows(user_id=user_id, hall_id=hall_id, show_name=show_name, about=about, genre=genre, rating=rating, time=time, left_seat=hall.size, ticketPrice=ticketPrice)
         db.session.add(new_show)
         db.session.commit()
         return "new_show", 201
      else:
         raise NotFoundError(status_code=404)
      



# api to get all halls

class getHallAPI(Resource):
   @marshal_with(hall_fields)
   def get(self):
      halls = Hall.query.all()
      return halls 



# api to get all shows

class getShowAPI(Resource):
   @marshal_with(Show_fields)  
   def get(self, hall_id):
      shows = Shows.query.filter_by(hall_id=hall_id).all()
      return shows
   

# API for managing bookings

booking_fields={
  "booking_id" : fields.Integer,
  "user_id" : fields.Integer,
  "hall_id" : fields.Integer,
  "show_id" : fields.Integer,
  "hall_name" : fields.String,
  "place" : fields.String,
  "show_name" : fields.String,
  "time" : fields.String,
  "n_tickets" : fields.Integer,
  "ticketPrice" : fields.Integer,
  "total_price" : fields.Integer,
}

update_booking_parser=reqparse.RequestParser()
update_booking_parser.add_argument('n_tickets')


create_booking_parser=reqparse.RequestParser()
create_booking_parser.add_argument('n_tickets')


class BookingManagerAPI(Resource):
   @marshal_with(booking_fields)
   @login_required
   def get(self, user_id):
      bookings=Bookings.query.filter_by(user_id=user_id).all()
      if bookings:
         return bookings
      else:
         return NotFoundError(status_code=404)
    

   @marshal_with(booking_fields)
   @login_required
   def put(self, user_id, hall_id, show_id, booking_id):
      args=update_booking_parser.parse_args()
      n_tickets=args.get("n_tickets", None)
      show=Shows.query.filter_by(show_id=show_id).first()

      if n_tickets is None:
         raise BookingsManagementError(status_code=400, error_code="BM1001", error_message="n_tickets is required")
    
      booking=Bookings.query.filter_by(user_id=user_id, hall_id=hall_id, show_id=show_id, booking_id=booking_id).first()
      if booking:
         booking.n_tickets=n_tickets
         booking.total_price=int(n_tickets) * int(show.ticketPrice)

         db.session.add(booking)
         db.session.commit()
         return booking
      else:
         raise NotFoundError(status_code=404)

   @login_required 
   def delete(self, user_id, hall_id, show_id, booking_id):
      booking=Bookings.query.filter_by(user_id=user_id, hall_id=hall_id, show_id=show_id, booking_id=booking_id).first()
      if booking:
         db.session.delete(booking)
         db.session.commit()
         return "", 200
      else:
         raise NotFoundError(status_code=404)
    
   @marshal_with(booking_fields)
   @login_required 
   def post(self, user_id, hall_id, show_id):
      args=create_booking_parser.parse_args()
      n_tickets=args.get("n_tickets", None)
      hall=Hall.query.filter_by(hall_id=hall_id).first()
      show=Shows.query.filter_by(show_id=show_id).first()

      if n_tickets is None:
         raise BookingsManagementError(status_code=400, error_code="BM1001", error_message="n_tickets is required")
      tp=int(n_tickets) * int(show.ticketPrice)
      new_booking=Bookings(user_id=user_id, hall_id=hall_id, show_id=show_id, hall_name=hall.hall_name, place=hall.place, show_name=show.show_name, time=show.time, n_tickets=n_tickets, ticketPrice=show.ticketPrice, total_price=tp)
      if int(show.left_seat) - int(n_tickets) >=0:
         db.session.add(new_booking)
         show.left_seat=int(show.left_seat)-int(n_tickets)
         db.session.commit()
         return new_booking, 201
      else:
         return 400
