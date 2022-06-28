from helper import Remove_Character, Get_Position_Value, Join_Value_With, Remove_Unusal_Spaces, Name_Attribute
import db_configuration
from pymongo import MongoClient
import pandas as pd
from scrapper import scrapper, overview, rankings, admission, academics, student_life, tuition_and_financial

# database connection setup
client = MongoClient(db_configuration.connection_str)
db = client.get_database(db_configuration.database)
college_db = db.colleges
print('Connection Status:\n',college_db)


# loading json file
lodeJson = open('unitId.json', "r")
uId_data = pd.read_json(lodeJson)
# print(uId_data)

status_count = db['status'].count_documents({})
print(status_count)

total_uid = len(uId_data)
print("Total University Count: ", total_uid)
scrap_data_count = status_count
number = status_count

domain_name = 'https://www.usnews.com/'
unable_scrap = 0

while number < 20:
# while number < total_uid:
    whole_data = {}     # container to store all the data
    flag = 0
    print('\n',number)
    perc = scrap_data_count/total_uid * 100
    print("Completed: {} %".format(perc))
    print("Data Scraped: ", scrap_data_count)
    print("Unable to scrap count: ", unable_scrap)
    print("Institution Name: ", uId_data["Institution Name"][number])
    uni_search_url = 'https://www.usnews.com/best-colleges/search?schoolName='
    uni_name = uId_data["Institution Name"][number]
    search_url = uni_search_url + uni_name
    print('Search URL: ', search_url)

    search_result_page, search_status = scrapper(search_url)
    if search_status == 200 :
        link = search_result_page.find('a', class_="card-name", href=True)
        if link != None:
            uni_link = link['href']
            uni_overview_url = domain_name + uni_link
            uni_rankings_url = uni_overview_url + '/overall-rankings'
            uni_admission_url = uni_overview_url + '/applying'
            uni_academics_url  = uni_overview_url + '/academics'
            uni_student_life_url  = uni_overview_url + '/student-life'
            uni_user_review_url  = uni_overview_url + '/reviews'
            uni_tution_and_fincance_url  = uni_overview_url + '/paying'
            uni_campus_url  = uni_overview_url + '/campus-info'

            # overview section
            # print(uni_overview_url)
            overview_page, overview_status = scrapper(uni_overview_url)
            if overview_status == 200:
                overview_section = overview(overview_page)
            
            # Rankings
            # print(uni_rankings_url)
            rankings_page, rankings_status = scrapper(uni_rankings_url)
            if rankings_status == 200:
                rankings_section = rankings(rankings_page)

            # Admission
            # print(uni_admission_url)
            admission_page, admission_status = scrapper(uni_admission_url)
            if admission_status == 200:
                admission_section, admission_contact_info = admission(admission_page)

            # Academics
            # print(uni_academics_url)
            academics_page, academics_status = scrapper(uni_academics_url)
            if academics_status == 200:
                academics_section = academics(academics_page)
            
            # Student Life
            # print(uni_student_life_url)
            student_life_page, student_life_status = scrapper(uni_student_life_url)
            if student_life_status == 200:
                student_life_section = student_life(student_life_page)

            # print(uni_user_review_url)

            # Tuition and Financial
            # print(uni_tution_and_fincance_url)
            tuition_and_financial_page, tuition_and_financial_status = scrapper(uni_tution_and_fincance_url)
            if tuition_and_financial_status == 200:
                tuition_and_financial_section = tuition_and_financial(tuition_and_financial_page)
            
            # print(uni_campus_url)
            whole_data['uid'] = int(uId_data["UnitID"][number])
            whole_data['institution_name'] = uId_data["Institution Name"][number]
            whole_data['overview_section'] = overview_section
            whole_data['rankings'] = rankings_section
            whole_data['admission'] = admission_section
            whole_data['academics'] = academics_section
            whole_data['student_life'] = student_life_section
            whole_data['tuition_and_financial'] = tuition_and_financial_section
            # print(whole_data)
            db['colleges'].insert_one(whole_data)

            db['admission_contact_information'].insert_one({
                'uid': int(uId_data["UnitID"][number]),
                'institution_name': uId_data["Institution Name"][number],
                'admission_contact_info': admission_contact_info,
            })

            db['status'].insert_one({
                'uid': int(uId_data["UnitID"][number]),
                'institution_name': uId_data["Institution Name"][number],
                'search_url': search_url,
                'uni_overview_url': uni_overview_url,
                'uni_rankings_url': uni_rankings_url,
                'uni_admission_url': uni_admission_url,
                'uni_academics_url': uni_academics_url,
                'uni_student_life_url': uni_student_life_url,
                'uni_user_review_url': uni_user_review_url,
                'uni_tution_and_fincance_url': uni_tution_and_fincance_url,
                'uni_campus_url': uni_campus_url,
                'search_status_code': search_status,
                'scrap_status': True,
            })
            print('Successfully Scrapped!!...')
        else:
            flag = 1
    else:
        flag = 1

    if flag == 1:
        unable_scrap = unable_scrap + 1
        print('unable_to_scrap')
        db['status'].insert_one({
            'uid': int(uId_data["UnitID"][number]),
            'institution_name': uId_data["Institution Name"][number],
            'search_url': search_url,
            'search_status_code': search_status,
            'scrap_status': False,
        })
    scrap_data_count = scrap_data_count + 1
    number = number + 1
