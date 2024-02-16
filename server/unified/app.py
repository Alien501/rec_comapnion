from flask import Flask
from flask import url_for
from flask_cors import CORS
import requests
import mysql.connector
import json

app = Flask(__name__)
cors = CORS(app)
app.secret_key = "secret"


def get_id(rollno):

    mydb = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        port=3306,
        database="users"
    )

    mycursor = mydb.cursor()
    get_user_query = "SELECT UNIFIED_ID from users where ROLLNO=%s"
    user_data = (rollno,)
    mycursor.execute(get_user_query, user_data)
    person_id = mycursor.fetchone()
    if person_id:
        print(f"person '{person_id}' exists.")
        mydb.close()
        return person_id[0]
    else:
        print(f"person '{person_id}' does not exist.")
        mydb.close()
        return -1



@app.route('/get-photo/<int:rollno>')
def get_photo(rollno):
    person_id = get_id(rollno)

    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '10%2C12',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonID': person_id,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/HRMS/ManageStaffStudent/UniPersonInfo.asmx/RetrievePersonPhoto',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    image = response.json()['d']
    data = {"image": image[1:-1]}
    return data


@app.route('/get-info/<int:rollno>')
def get_info(rollno):
    person_id = get_id(rollno)

    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '10%2C12',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonID': person_id,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx/GetPersonInfo',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    data = response.json()
    data = json.loads(data['d'])
    data = data[0]

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonID': person_id,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx/GetStuHeaderDetails',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    header = response.json()
    header = json.loads(header['d'])[0]
    data.update(header)
    return data

@app.route('/internal-marks/<int:rollno>')
def internal_marks(rollno):
    person_id = get_id(rollno)
    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '10%2C12',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonId': person_id,
        'Semester': 0,
        'Category': 0,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/HRMS/ManageStaffStudent/UniPersonInfo.asmx/BindInternalMarks',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    data = json.loads(response.json()['d'])
    """
    example data:
    {
        #sem
        1:[
        cat 1,{}
        cat 2,{}
        cat 3,{}
        ]
        2:[...]
    }
    """
    mod_data = {}
    for test in data:
        """
            'CATEST1'
            'CAT TEST1'
            'CAT TEST 1'
            'CATEST3(IIYEAR-FN)'
            'ASSIGNMENTI'
            unified backend was written by a bunch of monkeys while they were drunk and on meth.
            the fact that it works at all is a big achievement.
            In my opinion the servers that the code runs on should be cleansed with fire and whoever was in charge of
            desiging the api should just give up software development and move onto something better like becoming a farmer
            even then i don't think they can manage that.

            fuck it I am gonna just check if 'TEST' is in the string. or ASSIGNMENT
            and a cat number(1,2,3)

            CourseName	"B.Tech-IT"
            EventTitle	"2022-23/ODD/CA TEST 1 / II Year/Regular/UG"
            FirstName	"********"
            PersonId	*****
            SectionName	"A"
            Semester	"3"
            SubjName	"Software Engineering Essentials"
            Total	null
            U1	0
            U2	0
            U3	0
            U4	0
            U5  0

            sometimes they just like to return a fucking null.


        """
        title = test['EventTitle']
        test_sem = int(test['Semester'])
        total = test['Total']

        cat = title.split("/")[2]
        cat = cat.strip(" ").replace(" ", "")
        cat = cat.upper()

        cat_no = 0
        if 'CATEST' in cat:
            if '1' in cat:
                cat_no = 0
            if '2' in cat:
                cat_no = 1
            if '3' in cat:
                cat_no = 2

            if test_sem in mod_data.keys():
                if total:
                    mod_data[test_sem][cat_no].append(test)
            else:
                mod_data[test_sem] = [
                    [],  # cat 1
                    [],  # cat 2
                    [],  # cat 3
                ]
                if total:
                    mod_data[test_sem][cat_no].append(test)

    return mod_data


@app.route('/get-sems/<int:rollno>')
def get_sems(rollno):
    """
    app route: http://localhost/<rollno>/<sem>
    default sem: 0 -> gives the possible semesters
    returns numbers of semesters
    """
    person_id = get_id(rollno)

    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '0000000',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonId': person_id,
        'Semester': 0,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/HRMS/ManageStaffStudent/UniPersonInfo.asmx/BindSemester',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    data = response.json()
    data = json.loads(data['d'])

    return data


@app.route('/sem-marks/<int:rollno>/')
@app.route('/sem-marks/<int:rollno>/<int:sem>')
def semester_marks(rollno, sem=0):
    """
    app route: https://loalhost/<rollno>/<sem>
    <roll_no> user roll number is provided them their unified id is retrived from database
    <sem>
        0 - to retrieve all
        1 - semester 1
        .
        .
        .

    """
    person_id = get_id(rollno)
    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '0000000',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonId': person_id,
        'Semester': sem,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/HRMS/ManageStaffStudent/UniPersonInfo.asmx/BindGrade',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    data = response.json()
    data = json.loads(data['d'])
    """
    data modal: is gonna be easy for this unlinke internalmarks
    just an array of dict
    with each sem having their own dict array
    """
    mod_data = {}
    for sem in data:
        if sem['Semester'] in mod_data.keys():
            mod_data[sem['Semester']].append(sem)
        else:
            mod_data[sem['Semester']] = []
            mod_data[sem['Semester']].append(sem)

    return mod_data


# TODO
@app.route('/get-attendacne/<int:rollno>/')
def get_attendance(rollno):
    person_id = get_id(rollno)

    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '10%2C12',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'StartDate': '01-10-2023',
        'EndDate': '01-11-2023',
        'PersonID': person_id,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx/GetStudentAttendanceDetail',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    data = response.json()['d']
    data = json.loads(data)
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)