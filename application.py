from bs4 import BeautifulSoup
from flask import Flask, request,jsonify
import requests
weather = "https://weather.com/weather/monthly/l/60eb7796d033a593c3294ffa7d76578ee16343ee1b14bbab570b30eee2a0fb0e"
# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

@application.route("/david")
def david():
    return "415 Sucks"


@application.route("/weather")
def weather():
    return jsonify(getMonthlyWeather())


def getMonthlyWeather():
    page = requests.get(weather)

    parsedPage = BeautifulSoup(page.content, "html.parser")

    grid = parsedPage.find("div", class_= "Calendar--gridWrapper--1oa1f")
    temps = grid.find_all("div", class_= "CalendarDateCell--tempHigh--2VBba")
    days = grid.find_all("span", class_= "CalendarDateCell--date--3Fw3h")
    tempDic = []
    dayList = range(35)

    for i in (range(len(days))):
        tempDic.append({
            "day" : days[i].text,
            "temp" : temps[i].text
        })

    return tempDic

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()