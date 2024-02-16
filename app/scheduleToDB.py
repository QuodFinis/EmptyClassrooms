from app.models import Room, Schedule
from app.nacSchedule import schedule
from app import app, db


def schedToDB(schedule):
    with app.app_context():
        for day in schedule:
            for room_number, room_schedule in schedule[day].items():
                # Check if the room exists in the database
                room = Room.query.filter_by(number=room_number).first()

                # If the room doesn't exist, create a new room
                if not room:
                    room = Room(number=room_number)
                    db.session.add(room)
                    db.session.flush()

                # Add the schedule to the room
                for i in range(0, len(room_schedule), 2):
                    start_time = room_schedule[i]
                    end_time = room_schedule[i + 1]
                    schedule_obj = Schedule(day=day, start_time=start_time, end_time=end_time, room_id=room.id)
                    db.session.add(schedule_obj)

        db.session.commit()


schedToDB(schedule)
