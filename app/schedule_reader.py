from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import sys


def print_hi(name):
    print(f'Hi, {name}')


def round5(x):
    return 5 * round(x / 5)


def toMin(clock_time):
    Hour = clock_time[:clock_time.index(':')]
    Min = clock_time[clock_time.index(':') + 1: clock_time.index(':') + 3]
    AMPM = clock_time[clock_time.index(':') + 3: clock_time.index(':') + 5]
    mTime = (int(Hour) * 60) + int(Min)

    if AMPM == "PM" and Hour != "12":
        mTime += 720

    return round5(mTime)


def schedCleaner(building, schedule):
    for weekday in list(schedule.keys()):
        for classroom in list(schedule[weekday].keys()):
            if classroom.find(building):
                del schedule[weekday][classroom]

    return schedule


if __name__ == '__main__':
    print_hi('Joy')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.set_page_load_timeout(3)

    driver.get('https://globalsearch.cuny.edu/CFGlobalSearchTool/CFSearchToolController')

    college = driver.find_element(By.ID, "CTY01")
    college.click()
    term = Select(driver.find_element(By.NAME, "term_value"))
    term.select_by_visible_text("2023 Summer Term")
    nextPage = driver.find_element(By.NAME, "next_btn")
    nextPage.click()

    inPerson = driver.find_element(By.ID, "P")
    inPerson.click()
    hybrid = driver.find_element(By.ID, "HS")
    hybrid.click()
    showAll = driver.find_element(By.NAME, "open_class")
    showAll.click()
    numSubjects = len(Select(driver.find_element(By.NAME, "subject_name")).options)

    DayRoomTime = {"Mo": {}, "Tu": {}, "We": {}, "Th": {}, "Fr": {}, "Sa": {}, "Su": {}}

    building = 'NAC'

    for i in range(1, numSubjects):
        subject = Select(driver.find_element(By.NAME, "subject_name"))
        subject.select_by_index(i)
        search = driver.find_element(By.NAME, "search_btn_search")
        search.click()

        nacClasses = driver.find_elements(By.XPATH, "//*[contains(text(), '{}')]".format(building))

        if len(nacClasses) > 0:
            nacTimes = driver.find_elements(By.XPATH,
                                            "//*[contains(text(), '{}')]/preceding-sibling::td[1]".format(building))

            for j in range(0, len(nacClasses)):
                classrooms = nacClasses[j].get_attribute('innerHTML')[:-6].split('<br>')
                classtimes = nacTimes[j].get_attribute('innerHTML')[:-6].split('<br>')

                for k in range(len(classrooms)):
                    room = classrooms[k]
                    time = classtimes[k]

                    if not room.find(building):
                        classdays = time[:time.find(' ')]
                        classtime = time[time.find(' ') + 1:]

                        while classdays:
                            day = classdays[:2]

                            if not DayRoomTime[day].__contains__(room):
                                DayRoomTime[day][room] = []

                            times = DayRoomTime[day][room]

                            if toMin(classtime[:classtime.index(' ')]) not in times:
                                times.append(toMin(classtime[:classtime.index(' ')]))
                                times.append(toMin(classtime[classtime.index('-') + 2:]))
                                times = sorted(times)

                            classdays = classdays[2:]

        driver.back()

    stdoutOrigin = sys.stdout
    sys.stdout = open(r"C:\Users\mehed\Desktop\randproj\emptyClassroom\{}schedule.py".format(building), "w")

    print(DayRoomTime)

    sys.stdout.close()
    sys.stdout = stdoutOrigin

    schedCleaner(building, DayRoomTime)


    driver.close()
