from app.timeNow import getDayOfWeek, getToday
from app.nacSchedule import schedule

def toTime(minutes):
    hour = minutes // 60
    min = minutes - (hour * 60)
    ampm = "AM"

    if min < 10:
        min = "0" + str(min)

    if hour >= 12:
        ampm = "PM"
        if hour > 12:
            hour -= 12

    time = "{}:{}{}".format(hour, min, ampm)
    return time


def addTime(dictionary, time, room):
    if time not in dictionary.keys():
        dictionary[time] = []

    dictionary[time].append(room)


def freeClasses(schedule, floor=None):
    today = getToday()
    dayOfWeek = getDayOfWeek()

    if dayOfWeek in ['Su', 'Sa']:
        return "It's the weekend!"

    minutesNow = today.hour * 60 + today.minute
    time_room = {}
    room_time = {}

    for room in schedule[dayOfWeek].keys():
        if floor and f" {floor}/" not in room:
            continue

        times = schedule[dayOfWeek][room]

        if minutesNow > times[-1]:
            room_time[room] = ("{} has no more classes".format(room))
            addTime(time_room, 1200, room)

        elif minutesNow < times[0]:
            room_time[room] = "{} next class begins at {}".format(room, toTime(times[0]))
            addTime(time_room, times[0], room)

        else:
            for i in range(1, len(times) - 1, 2):
                if times[i] <= minutesNow <= times[i + 1]:
                    room_time[room] = "{} next class begins at {}".format(room, toTime(times[i + 1]))
                    addTime(time_room, times[i + 1], room)
                    break

    classList = [toTime(minutesNow)]
    for time in reversed(sorted(time_room.keys())):
        for room in time_room[time]:
            classList.append(room_time[room])

    return classList



def run(floor):
    return freeClasses(schedule, floor=floor)


if __name__ == '__main__':
    print(run())
