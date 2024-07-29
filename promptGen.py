import xml.etree.ElementTree as ET
from collections import defaultdict

def find_xbrl_tags(parent, xbrlDict):
    for child in parent:
        if 'us-gaap' in child.tag:
            tag = child.tag.split('}')[-1]
            xbrlDict[tag].append({
                'value': child.text.strip() if child.text else '', 
                'contextRef': child.get('contextRef', '')
            })
        find_xbrl_tags(child, xbrlDict)

def scrape_xbrl(path):
    tree = ET.parse(path)
    root = tree.getroot()
    xbrlDict = defaultdict(list)
    find_xbrl_tags(root, xbrlDict)
    return xbrlDict

path = 'SEC_Filings/aapl-20190928/a10-k20199282019_htm.xml'
company = 'Apple'
years = range(2019, 2023)
xbrlData = scrape_xbrl(path)

def generate_questions(questionFormats):

    questionsForCompany = []
    questionsList = []

    for q in questionFormats:
        questionsForCompany.append(q.replace('[company name]', company))

    for q in questionsForCompany:
        for concept in xbrlData:
            question = q.replace('[financial concept]', concept)
            for year in years:
                question = question.replace('[year]', str(year))
                questionsList.append(question)
    # print(questionsList)
    return questionsList

questionFormats = [
    "What is the value of [company name]'s [financial concept] for the fiscal year ending [year]?",
    "Can you provide the value for [financial concept] from [company name] for the year ending [year]?",
    "How much was [company name]'s [financial concept] for the fiscal period concluding in [year]?",
    "What was the reported value of [financial concept] for [company name] at the end of the fiscal year [year]?",
    "Please find the fiscal year [year] value of [financial concept] for [company name]."
]

allQuestions = generate_questions(questionFormats)

output_file = "queries.txt"
with open(output_file, 'w') as file:
    for question in enumerate(allQuestions, 1):
        file.write(f"{question}\n")
