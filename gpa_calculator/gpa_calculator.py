import env
import click
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# auxiliary dictionary used to convert grade points to numerical values
GRADE_TO_NUMERIC = {
    'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C+': 5,
    'C': 4, 'D+': 3, 'D': 2, 'E': 1, 'F': 0
}


def parse_grades_file(cumulative):
    """
    Parse .grades file into a dictionary

    :param cumulative: type of gpa requested
    :return: dictionary of taken courses along with its course_credit and grade obtained
    """

    # define conditions for the type of GPA requested
    if cumulative:
        # only pick courses that have already been taken
        # courses that are currently being taken have a ' ' at position 25
        scheme = lambda line: line[25] != ' '
    else:
        # only pick EECS courses that have already been taken and omit ones with second letter 5
        scheme = lambda line: line[25] != ' ' and 'EECS' in line and line[16] != '5'

    # read .grades file
    with open('.grades') as f:
        contents = f.readlines()

    # parse contents of .grades file
    courses = {}  # dictionary containing course_name, course_credit and grade
    contents = contents[1:]  # remove header of file
    for c in contents:
        # remove unwanted chars 
        c = c.replace('\n', '').replace('\t', ' ')

        if scheme(c):
            c = c.split(' ')
            name = c[1] + ' ' + c[2]  # name = 'faculty/dept course_code'
            course_credit = c[3]
            grade = c[4]

            if name == 'LE/EECS 1001':  # this was a pass/fail course
                continue

            courses[name] = {'course_credit': course_credit, 'grade': grade}

    return courses


def display_web(cumulative):
    """
    Display GPA calculator in a browser for an interactive interface

    :param cumulative: type of GPA requested
    :return: None
    """

    # navigate to url
    driver = webdriver.Chrome(env.webdriver_location)
    url = 'https://laps.yorku.ca/student-resources/gpa-calculator'
    driver.get(url)

    # parse .grades file to obtain dictionary of courses taken
    courses = parse_grades_file(cumulative)

    # find table to inject data
    rows = driver.find_element_by_name('form1').find_element_by_xpath("table/tbody").find_elements_by_tag_name('tr')
    rows = rows[2:len(courses) + 2]  # first two rows are un-editable

    # inject data into web page
    for row, course_name in zip(rows, courses):
        # columns to inject name, number of credits and grade
        cols = row.find_elements_by_xpath('td/div/input')[:2]  # name, credits
        cols += row.find_elements_by_xpath('td/div/select')
        cols[0].send_keys(course_name)  # inject course_name
        cols[1].send_keys(courses[course_name]['course_credit'])  # inject course_credit
        Select(cols[2]).select_by_visible_text(courses[course_name]['grade'])  # inject grade

    # click to compute button to find GPA
    driver.find_element_by_name('BUTTON').click()
    input()


def display_cli(cumulative):
    """
    Display GPA within a cli interface

    :param cumulative: type of GPA requested
    :return: None
    """

    # parse .grades file to obtain dictionary of courses taken
    courses = parse_grades_file(cumulative)

    total_grade_points = 0
    total_credits = 0
    for c_name, c_details in courses.items():
        c_grade = c_details['grade']
        c_credits = float(c_details['course_credit'])

        total_grade_points += GRADE_TO_NUMERIC[c_grade] * c_credits
        total_credits += c_credits

    gpa = total_grade_points / total_credits

    gpa_type = 'cumulative' if cumulative else 'core'
    print('Your %s GPA is %.2f' % (gpa_type, gpa))
    input()


@click.command()
@click.option('--web/--cli')
@click.option('--cumulative/--core')
def main(web, cumulative):
    """
    Controller for interface and GPA preferences

    :param web: boolean flag for displaying within a browser or CLI
    :param cumulative: boolean flag for type of GPA requested
    :return: None
    """
    if web:
        display_web(cumulative)
    else:
        display_cli(cumulative)


if __name__ == '__main__':
    main()
