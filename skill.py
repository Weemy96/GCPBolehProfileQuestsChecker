from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
from datetime import datetime, timedelta
import re
import sys

if len(sys.argv) < 2:
    boostskillProfile_URL = input('Input your Google Cloud Skills Boost Profile URL: ')
else:
    boostskillProfile_URL = sys.argv[1]

# Define the date range
start_date_str = "Apr 25, 2024"
end_date_str   = "May 24, 2024"


# Define the time zone abbreviation and its corresponding offset
timezone_abbrev = "EDT"
timezone_offset = timedelta(hours=-4)  # EDT is UTC-4


# Parse the date range
start_date = datetime.strptime(start_date_str, "%b %d, %Y") + timezone_offset
end_date = datetime.strptime(end_date_str, "%b %d, %Y") + timezone_offset

webpage = requests.get(boostskillProfile_URL, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(webpage.content, 'html.parser')

quests_requested = [
# AI/ML:
# Skill Badges
"Classify Images with TensorFlow on Google Cloud",
"Build LookML Objects in Looker",
"Detect Manufacturing Defects using Visual Inspection AI",
"Analyze Speech and Language with Google APIs",
"Analyze Images with the Cloud Vision API",
"Analyze Sentiment with Natural Language API",
"Perform Predictive Data Analysis in BigQuery",
"Create ML Models with BigQuery ML",
 
# Regular Badges
"Integrating Applications with Gemini 1.0 Pro on Google Cloud",
"Intro to ML: Language Processing",
"Intro to ML: Image Processing",
"Generative AI Explorer - Vertex AI",
"Introduction to AI and Machine Learning on Google Cloud",
"Google Cloud Big Data and Machine Learning Fundamentals",
"Applying Machine Learning to your Data with Google Cloud",
"Production Machine Learning Systems",
"Smart Analytics, Machine Learning, and AI on Google Cloud",
"ML Pipelines on Google Cloud",
"Gemini for Data Scientists and Analysts",

# Infrastructure & Security:,
# Skill Badges
"Create and Manage AlloyDB Instances",
"Create and Manage Cloud SQL for PostgreSQL Instances",
"Monitor and Manage Google Cloud Resources",
"Manage Kubernetes in Google Cloud",
"Build Infrastructure with Terraform on Google Cloud",
 
# Regular Badges
"Baseline: Infrastructure",
"Google Cloud Computing Foundations: Infrastructure in Google Cloud - Locales",
"Security Best Practices in Google Cloud",
"Securing your Network with Cloud Armor",
"Google Cloud Computing Foundations: Networking and Security in Google Cloud",
"Mitigating Security Vulnerabilities on Google Cloud"
]

must_done_quests_requested = [
# Skill Badges
"Classify Images with TensorFlow on Google Cloud",
"Build LookML Objects in Looker",
"Detect Manufacturing Defects using Visual Inspection AI",
"Analyze Speech and Language with Google APIs",
"Analyze Images with the Cloud Vision API",
"Analyze Sentiment with Natural Language API",
"Perform Predictive Data Analysis in BigQuery",
"Create ML Models with BigQuery ML",

# Infrastructure & Security:,
# Skill Badges
"Create and Manage AlloyDB Instances",
"Create and Manage Cloud SQL for PostgreSQL Instances",
"Monitor and Manage Google Cloud Resources",
"Manage Kubernetes in Google Cloud",
"Build Infrastructure with Terraform on Google Cloud"
]

skill = []
date_comp = []
total_match = 0
#### corse name
for span in soup.findAll('span', {'class':'ql-title-medium l-mts'}):
    quests_completed = span.get_text().replace('\n','')
    # print(quests_requested)
    skill.append(quests_completed)
### corse complete date
for span in soup.findAll('span', {'class':'ql-body-medium l-mbs'}):
    date_comp.append(span.get_text().replace('\n',''))
result = zip(skill,date_comp)


# Filter and only show entries between the start and end dates
filtered_data = []
for entry in result:
    date_match = re.search(r"(\w{3} \d{1,2}, \d{4})", entry[1])
    if date_match:
        date_str = date_match.group(1)
        date_with_timezone = datetime.strptime(date_str, "%b %d, %Y") + timezone_offset
        if start_date <= date_with_timezone <= end_date:
            filtered_data.append(entry)

print(tabulate(filtered_data,headers=["Quest Completed","Date of Complete"]))
print("\nTotal: %d\n\n"%len(filtered_data))

#Filter only match of quests_requested
matched_entries = [entry for entry in filtered_data if any(skill in entry[0] for skill in quests_requested)]


print(tabulate(matched_entries,headers=["Quest Metched","Date of Complete"]))
print("\nTotal: "+ str(len(matched_entries)))

must_done_count = [entry for entry in filtered_data if any(skill in entry[0] for skill in must_done_quests_requested)]
print("Total Skill badges: %s"%len(must_done_count))
if(len(must_done_count) >= 6):
    print("✅ Complete with requested Skill badges.")
else:
    print("❌ Not requested, must done with 6 skill badges, you currently in %s. 💪 Keep going."%str(len(must_done_count)))

if(len(matched_entries)<= 0):
    print("Maybe your Profile URL wrong / Profile URL not public and accessible / Not earned the badge")