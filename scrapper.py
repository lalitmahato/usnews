import requests
from bs4 import BeautifulSoup
from helper import Remove_Character, Get_Position_Value, Join_Value_With, Remove_Unusal_Spaces, Name_Attribute, Get_href

def scrapper(url):
    page = requests.get(url, timeout=1000, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content,'html.parser')
    return (soup, page.status_code)

def overview(page):
    overview_section = {}
    overview_intro = page.find('div', class_='Raw-slyvem-0 util__RawContent-sc-1kd04gx-2 RClcr eNQGvA').p.text
    general_info = page.find_all('div', class_='Box-w0dun1-0 DataRow__Row-sc-1udybh3-0 knONpq keLhhz')
    general_information = {}
    for gi in general_info:
        paragraphs = gi.find_all('p')
        if len(paragraphs) == 2:
            general_information[Name_Attribute(paragraphs[0])] = paragraphs[1].text
        elif len(paragraphs) == 1:
            general_information[Name_Attribute(paragraphs[0])] = Get_href(gi)

    overview_section['overview'] = overview_intro
    overview_section['general_information'] = general_information
    return overview_section

def rankings(page):
    rankings_section = []
    rankings = page.find_all('a', class_='Anchor-byh49a-0 PlBer')
    for r in rankings:
        rank = {}
        ranks = r.find_all('strong')
        if len(ranks) == 2:
            rank['url'] = r['href']
            rank['rank'] = ranks[0].text
            rank['title'] = ranks[1].text
            rankings_section.append(rank)
    return rankings_section

def admission(admission_page):
    admission_section = {}
    summary_box = admission_page.find('div', class_='summary-box')
    summary = summary_box.find_all('p')
    paragraph = ''
    for p in summary:
        paragraph = paragraph + Remove_Unusal_Spaces(p)
    
    admission_info = admission_page.find_all('div', class_='Box-w0dun1-0 DataRow__Row-sc-1udybh3-0 knONpq fPkWrz Display__DataRowBox-h3gn08-1 kwTiaI')
    admission_information = {}
    for info in admission_info:
        para = info.find_all('p')
        if (para[0].text != 'UNLOCK WITH COMPASS') & (len(para) == 2):
            admission_information[Name_Attribute(para[0])] = para[1].text
    
    admission_contact_section = admission_page.find('div', class_='Box-w0dun1-0 DataRow__Row-sc-1udybh3-0 knONpq fPkWrz Display__DataRowBox-h3gn08-1 kwTiaI datarow-list')
    contact_section = admission_contact_section.find_all('div')
    admission_contact_info = [Remove_Unusal_Spaces(i)  for i in contact_section]
    # admission_contact_info['name'] = Remove_Unusal_Spaces(contact_section[0])
    # admission_contact_info['office'] = Remove_Unusal_Spaces(contact_section[1])
    # admission_contact_info['phone_number'] = Remove_Unusal_Spaces(contact_section[2])
    # admission_contact_info['email'] = Remove_Unusal_Spaces(contact_section[3])

    admission_section['summary'] = paragraph
    admission_section['admission_information'] = admission_information
    admission_section['admission_contact_information'] = admission_contact_info

    return (admission_section, admission_contact_info)

def academics(academics_page):
    academics_section = {}
    academic_summary_box = academics_page.find('div', class_='summary-box')
    academic_summary = academic_summary_box.find_all('p')
    academic_paragraph = ''
    for p in academic_summary:
        academic_paragraph = academic_paragraph + Remove_Unusal_Spaces(p)

    most_popular_majors = []
    popular_majors = academics_page.find('div', class_='Box-w0dun1-0 DataRow__Row-sc-1udybh3-0 knONpq fPkWrz Display__DataRowBox-h3gn08-1 kwTiaI datarow-table truncated')
    if popular_majors != None:
        pop_majors = popular_majors.find_all('li')
        for m in pop_majors:
            para = m.find_all('p')
            if len(para) == 2:
                most_popular_majors.append({
                    'name': para[0].text,
                    'percentage': para[1].text
                })
    academics_section['academic_summary'] = academic_paragraph
    academics_section['popular_majors'] = most_popular_majors
    return academics_section

def student_life(student_life_page):
    student_life_section = {}
    student_life_summary_box = student_life_page.find('div', class_='summary-box')
    student_life_summary = student_life_summary_box.find_all('p')
    student_life_paragraph = ''
    for p in student_life_summary:
        student_life_paragraph = student_life_paragraph + Remove_Unusal_Spaces(p)
    uni_student_body = []
    student_body = student_life_page.find_all('div', class_='Box-w0dun1-0 DataRow__Row-sc-1udybh3-0')
    for stud in student_body:
        para = stud.find_all('p')
        if (len(para) == 2) & (para[0].text != 'UNLOCK WITH COMPASS'):
            uni_student_body.append({
                'title': para[0].text,
                'value': para[1].text,
            })
    student_life_section['student_life_summary'] = student_life_paragraph
    student_life_section['student_life_information'] = uni_student_body
    return student_life_section

def tuition_and_financial(tuition_and_financial_page):
    tuition_and_financial_section = {}
    tuition_and_financial_summary_box = tuition_and_financial_page.find('div', class_='summary-box')
    tuition_and_financial_summary = tuition_and_financial_summary_box.find_all('p')
    tuition_and_financial_paragraph = ''
    for p in tuition_and_financial_summary:
        tuition_and_financial_paragraph = tuition_and_financial_paragraph + Remove_Unusal_Spaces(p)
    
    financial_info = []
    finance = tuition_and_financial_page.find_all('div', class_='Box-w0dun1-0 DataRow__Row-sc-1udybh3-0 knONpq fPkWrz Display__DataRowBox-h3gn08-1 kwTiaI')
    for f in finance:
        para = f.find_all('p')
        if (len(para) == 2) & (para[0].text != 'UNLOCK WITH COMPASS'):
            financial_info.append({
                'titel': para[0].text,
                'value': para[1].text,
            })

    tuition_and_financial_section['summary'] = tuition_and_financial_paragraph
    tuition_and_financial_section['financial_information'] = financial_info
    return tuition_and_financial_section