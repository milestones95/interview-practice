import datetime, timedelta from datetime

class Booking_System:

    def __init__(self):
        self.bookings = {}

    # 9am - 10am, 10am-10:30am, 1pm - 2:30pm. What about the request 10:20am - 11am?
    # 10:20 starts before the 10:30am ends. I looked at the end time. 
    # what about 4pm-5pm? there is no meeting that ends after 4 pm so it should be okay. 
    # what about the edge case if a meeting starts at 3pm and ends the following day at 3pm.
    # in this case the end time of the meeting would be after the 4 clock slot and we would know that if we include the date in the end time not just the hour/minute
    # it needs to either start after one of the end times and end before the start times
    # 2-4pm is taken. can i book for 1-2pm? yes becuase the end time is before the 2-4pm start time. but the start time is also after the end times.
    # if the end time is after my start time, check to see if the start time is after my end time. if it is then i can book it. if not then i can't book it.
    # we can do this in o(n) time making the room id the key and the values being the 
    # my start: 8am-9:20 am. booking is 9-10am. 8 start is less than booking start and booking end. My end time is greater than booking start


    def request_booking(self, room_id: str, start_time: datetime, end_time: datetime):

        bookings = self.bookings.get(room_id,[])

        ## the bookings are a tuple of (start,end)


        for b in bookings:
            s,e = b

            if end_time  > s and start_time < e:
                throw error

        self.bookings.setDefault(room_id, []).append(start_time, end_time)


    # I want bookings for tuesday:
    # Monday 4pm-Tuesday 1am
    # monday 3pm-330pm
    # Tuesday 3pm-5pm
    # wednesday 1am-2am
    # if end date is before wednesday and the end date is >= the start of tuesday
    def list_bookings(self, room_id: str, day: datetime):

        start_of_today = datetime.combine(day, time.min)
        taken = []
        bookings = self.bookings.get(room_id,[])
            
        for booking in bookings:
            s,e = booking

            if s < start_of_today + timedelta(hours=24) and start_of_today < e:
                taken.append((s,e))

        return taken


