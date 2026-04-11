from flask import Flask, request, jsonify, render_template
import os
import io
import re

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

KNOWN_SKILLS = [
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'ruby',
    'swift', 'kotlin', 'scala', 'php', 'perl', 'r', 'matlab',
    'react', 'angular', 'vue', 'next.js', 'nuxt', 'svelte', 'jquery', 'html', 'css',
    'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'spring boot',
    'rails', 'laravel', 'asp.net', '.net',
    'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite',
    'sql', 'nosql', 'oracle', 'cassandra', 'dynamodb',
    'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
    'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'gitlab',
    'github', 'git', 'ci/cd', 'devops', 'linux', 'unix', 'bash', 'shell',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
    'scikit-learn', 'pandas', 'numpy', 'data science', 'data analysis',
    'hadoop', 'spark', 'kafka', 'airflow', 'data engineering',
    'tableau', 'power bi', 'looker', 'excel', 'analytics',
    'unity', 'unreal', 'game development', 'opengl', 'vulkan',
    'ios', 'android', 'react native', 'flutter', 'mobile development',
    'cybersecurity', 'network', 'firewalls', 'penetration testing',
    'blockchain', 'solidity', 'web3', 'nft', 'smart contracts',
    'rest api', 'graphql', 'grpc', 'microservices', 'soap',
    'agile', 'scrum', 'kanban', 'jira', 'confluence',
    'selenium', 'cypress', 'jest', 'pytest', 'junit', 'testing', 'qa',
    'ui/ux', 'figma', 'sketch', 'adobe xd', 'design',
    'sap', 'salesforce', 'erp', 'crm',
    'embedded', 'iot', 'arduino', 'raspberry pi', 'fpga',
    'nlp', 'computer vision', 'opencv', 'bert', 'gpt',
    'objective-c', 'firebase', 'xcode', 'cobol', 'mainframe',
]

JOBS_DATA = {
    'new york': [
        {'id':1,'role':'Senior Python Developer','openings':450,'salary':'$120,000 - $160,000','salary_min':120000,'salary_max':160000,'skills':['Python','Django','PostgreSQL','AWS'],'company':'Various Tech','experience':'3-5 yrs','type':'Full-time','growth':9,'score':88,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':3},
        {'id':2,'role':'Cloud Architect','openings':320,'salary':'$130,000 - $180,000','salary_min':130000,'salary_max':180000,'skills':['AWS','Kubernetes','Terraform','DevOps'],'company':'Various','experience':'5-8 yrs','type':'Full-time','growth':9,'score':92,'category':['high_pay','best'],'tags':['Money','Star'],'posted_days_ago':5},
        {'id':3,'role':'ML Engineer','openings':280,'salary':'$140,000 - $190,000','salary_min':140000,'salary_max':190000,'skills':['Python','TensorFlow','PyTorch','Data Science'],'company':'Various','experience':'3-6 yrs','type':'Full-time','growth':10,'score':95,'category':['high_pay','best'],'tags':['Money','Star'],'posted_days_ago':1},
        {'id':4,'role':'Frontend Developer','openings':380,'salary':'$90,000 - $130,000','salary_min':90000,'salary_max':130000,'skills':['React','JavaScript','CSS','TypeScript'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':7,'score':75,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':2},
        {'id':5,'role':'DevOps Engineer','openings':250,'salary':'$110,000 - $150,000','salary_min':110000,'salary_max':150000,'skills':['Docker','Kubernetes','CI/CD','Linux'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':8,'score':82,'category':['high_demand','high_pay'],'tags':['Fire','Money'],'posted_days_ago':4},
        {'id':6,'role':'QA Engineer','openings':120,'salary':'$70,000 - $100,000','salary_min':70000,'salary_max':100000,'skills':['Selenium','Testing','Automation','Python'],'company':'Various','experience':'2-3 yrs','type':'Full-time','growth':4,'score':55,'category':['risky'],'tags':['Warning'],'posted_days_ago':10},
        {'id':7,'role':'Cybersecurity Analyst','openings':60,'salary':'$100,000 - $145,000','salary_min':100000,'salary_max':145000,'skills':['Cybersecurity','Network','Firewalls','Linux'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':88,'category':['emergency'],'tags':['Alarm'],'posted_days_ago':1},
        {'id':8,'role':'Data Engineer','openings':310,'salary':'$115,000 - $155,000','salary_min':115000,'salary_max':155000,'skills':['Spark','Python','SQL','Kafka'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':87,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':2},
        {'id':9,'role':'Blockchain Developer','openings':55,'salary':'$130,000 - $175,000','salary_min':130000,'salary_max':175000,'skills':['Blockchain','Solidity','Web3','Smart Contracts'],'company':'FinTech Startups','experience':'2-4 yrs','type':'Full-time','growth':6,'score':65,'category':['risky','new'],'tags':['Warning','New'],'posted_days_ago':1},
        {'id':10,'role':'Site Reliability Engineer','openings':52,'salary':'$125,000 - $165,000','salary_min':125000,'salary_max':165000,'skills':['Linux','Python','AWS','Monitoring'],'company':'Various','experience':'4-6 yrs','type':'Full-time','growth':8,'score':84,'category':['emergency','new'],'tags':['Alarm','New'],'posted_days_ago':2},
    ],
    'bangalore': [
        {'id':1,'role':'Java Developer','openings':520,'salary':'\u20b912,00,000 - \u20b918,00,000','salary_min':1200000,'salary_max':1800000,'skills':['Java','Spring Boot','Microservices','SQL'],'company':'Various MNCs','experience':'2-5 yrs','type':'Full-time','growth':8,'score':82,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':3},
        {'id':2,'role':'Data Engineer','openings':380,'salary':'\u20b914,00,000 - \u20b920,00,000','salary_min':1400000,'salary_max':2000000,'skills':['Spark','Hadoop','Python','Scala'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':90,'category':['high_demand','high_pay','best'],'tags':['Fire','Money','Star'],'posted_days_ago':2},
        {'id':3,'role':'Full Stack Developer','openings':450,'salary':'\u20b913,00,000 - \u20b919,00,000','salary_min':1300000,'salary_max':1900000,'skills':['React','Node.js','MongoDB','JavaScript'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':8,'score':83,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':1},
        {'id':4,'role':'ML Engineer','openings':300,'salary':'\u20b916,00,000 - \u20b925,00,000','salary_min':1600000,'salary_max':2500000,'skills':['Python','TensorFlow','PyTorch','NLP'],'company':'Various','experience':'2-5 yrs','type':'Full-time','growth':10,'score':95,'category':['high_pay','best'],'tags':['Money','Star'],'posted_days_ago':1},
        {'id':5,'role':'Android Developer','openings':280,'salary':'\u20b910,00,000 - \u20b915,00,000','salary_min':1000000,'salary_max':1500000,'skills':['Kotlin','Android','Java','Firebase'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':6,'score':68,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':5},
        {'id':6,'role':'iOS Developer','openings':220,'salary':'\u20b911,00,000 - \u20b916,00,000','salary_min':1100000,'salary_max':1600000,'skills':['Swift','iOS','Xcode','Objective-C'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':6,'score':65,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':6},
        {'id':7,'role':'Business Analyst','openings':150,'salary':'\u20b98,00,000 - \u20b912,00,000','salary_min':800000,'salary_max':1200000,'skills':['SQL','Excel','Tableau','Analytics'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':4,'score':50,'category':['risky'],'tags':['Warning'],'posted_days_ago':12},
        {'id':8,'role':'SAP Consultant','openings':45,'salary':'\u20b915,00,000 - \u20b922,00,000','salary_min':1500000,'salary_max':2200000,'skills':['SAP','ERP','ABAP','Consulting'],'company':'IT Services','experience':'5-8 yrs','type':'Full-time','growth':3,'score':45,'category':['emergency','risky'],'tags':['Alarm','Warning'],'posted_days_ago':7},
        {'id':9,'role':'Cloud DevOps Engineer','openings':52,'salary':'\u20b914,00,000 - \u20b920,00,000','salary_min':1400000,'salary_max':2000000,'skills':['AWS','Kubernetes','Docker','Terraform'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':88,'category':['emergency','new'],'tags':['Alarm','New'],'posted_days_ago':2},
        {'id':10,'role':'Cybersecurity Engineer','openings':55,'salary':'\u20b915,00,000 - \u20b922,00,000','salary_min':1500000,'salary_max':2200000,'skills':['Cybersecurity','Network','Penetration Testing','Linux'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':90,'category':['emergency','new','best'],'tags':['Alarm','New','Star'],'posted_days_ago':1},
    ],
    'london': [
        {'id':1,'role':'Senior Java Developer','openings':380,'salary':'\u00a370,000 - \u00a3100,000','salary_min':70000,'salary_max':100000,'skills':['Java','Spring','Microservices','Docker'],'company':'Various','experience':'4-7 yrs','type':'Full-time','growth':7,'score':80,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':2},
        {'id':2,'role':'Data Scientist','openings':290,'salary':'\u00a375,000 - \u00a3110,000','salary_min':75000,'salary_max':110000,'skills':['Python','R','Machine Learning','SQL'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':90,'category':['high_pay','best'],'tags':['Money','Star'],'posted_days_ago':3},
        {'id':3,'role':'DevOps Engineer','openings':250,'salary':'\u00a365,000 - \u00a395,000','salary_min':65000,'salary_max':95000,'skills':['AWS','Kubernetes','Terraform','Python'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':8,'score':83,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':4},
        {'id':4,'role':'Frontend Developer','openings':320,'salary':'\u00a350,000 - \u00a380,000','salary_min':50000,'salary_max':80000,'skills':['React','JavaScript','Vue','HTML/CSS'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':6,'score':70,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':1},
        {'id':5,'role':'Backend Developer','openings':280,'salary':'\u00a355,000 - \u00a385,000','salary_min':55000,'salary_max':85000,'skills':['Node.js','Python','Java','REST API'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':7,'score':75,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':2},
        {'id':6,'role':'Junior Developer','openings':200,'salary':'\u00a330,000 - \u00a350,000','salary_min':30000,'salary_max':50000,'skills':['JavaScript','Python','Git','Basics'],'company':'Various','experience':'0-2 yrs','type':'Full-time','growth':7,'score':60,'category':['new'],'tags':['New'],'posted_days_ago':1},
        {'id':7,'role':'Fintech Developer','openings':55,'salary':'\u00a380,000 - \u00a3120,000','salary_min':80000,'salary_max':120000,'skills':['Python','Java','Blockchain','APIs'],'company':'FinTech','experience':'3-6 yrs','type':'Full-time','growth':8,'score':87,'category':['emergency','high_pay'],'tags':['Alarm','Money'],'posted_days_ago':2},
        {'id':8,'role':'Legacy COBOL Developer','openings':40,'salary':'\u00a360,000 - \u00a390,000','salary_min':60000,'salary_max':90000,'skills':['COBOL','Mainframe','SQL','Banking'],'company':'Banks','experience':'5+ yrs','type':'Full-time','growth':2,'score':30,'category':['risky','emergency'],'tags':['Warning','Alarm'],'posted_days_ago':15},
        {'id':9,'role':'AI/ML Engineer','openings':260,'salary':'\u00a380,000 - \u00a3120,000','salary_min':80000,'salary_max':120000,'skills':['Python','TensorFlow','PyTorch','NLP'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':10,'score':95,'category':['high_pay','best','new'],'tags':['Money','Star','New'],'posted_days_ago':2},
        {'id':10,'role':'Cloud Security Engineer','openings':52,'salary':'\u00a375,000 - \u00a3110,000','salary_min':75000,'salary_max':110000,'skills':['AWS','Azure','Cybersecurity','Terraform'],'company':'Various','experience':'4-6 yrs','type':'Full-time','growth':9,'score':90,'category':['emergency','new'],'tags':['Alarm','New'],'posted_days_ago':3},
    ],
    'dubai': [
        {'id':1,'role':'Cloud Solutions Architect','openings':310,'salary':'AED 200,000 - 300,000','salary_min':200000,'salary_max':300000,'skills':['AWS','Azure','GCP','Terraform'],'company':'Various','experience':'5-8 yrs','type':'Full-time','growth':9,'score':90,'category':['high_demand','high_pay','best'],'tags':['Fire','Money','Star'],'posted_days_ago':2},
        {'id':2,'role':'Full Stack Developer','openings':420,'salary':'AED 150,000 - 220,000','salary_min':150000,'salary_max':220000,'skills':['React','Node.js','MongoDB','Docker'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':8,'score':82,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':1},
        {'id':3,'role':'Data Analyst','openings':280,'salary':'AED 140,000 - 200,000','salary_min':140000,'salary_max':200000,'skills':['Python','SQL','Tableau','Power BI'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':7,'score':78,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':3},
        {'id':4,'role':'Cybersecurity Engineer','openings':200,'salary':'AED 180,000 - 280,000','salary_min':180000,'salary_max':280000,'skills':['Cybersecurity','Linux','Network','Firewalls'],'company':'Various','experience':'4-6 yrs','type':'Full-time','growth':9,'score':88,'category':['high_pay','best','emergency'],'tags':['Money','Star','Alarm'],'posted_days_ago':4},
        {'id':5,'role':'IT Support','openings':150,'salary':'AED 80,000 - 120,000','salary_min':80000,'salary_max':120000,'skills':['Windows','Linux','Networking','Troubleshooting'],'company':'Various','experience':'1-3 yrs','type':'Full-time','growth':3,'score':40,'category':['risky'],'tags':['Warning'],'posted_days_ago':8},
        {'id':6,'role':'Blockchain Developer','openings':55,'salary':'AED 200,000 - 300,000','salary_min':200000,'salary_max':300000,'skills':['Blockchain','Solidity','Web3','Smart Contracts'],'company':'Web3 Startups','experience':'2-4 yrs','type':'Full-time','growth':7,'score':75,'category':['emergency','new','high_pay'],'tags':['Alarm','New','Money'],'posted_days_ago':2},
        {'id':7,'role':'SAP FICO Consultant','openings':45,'salary':'AED 160,000 - 240,000','salary_min':160000,'salary_max':240000,'skills':['SAP','FICO','ERP','Finance'],'company':'Big4','experience':'5-8 yrs','type':'Full-time','growth':3,'score':42,'category':['risky','emergency'],'tags':['Warning','Alarm'],'posted_days_ago':20},
        {'id':8,'role':'ML Engineer','openings':180,'salary':'AED 200,000 - 300,000','salary_min':200000,'salary_max':300000,'skills':['Python','TensorFlow','PyTorch','Data Science'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':10,'score':93,'category':['high_pay','best','new'],'tags':['Money','Star','New'],'posted_days_ago':3},
        {'id':9,'role':'ERP Consultant','openings':100,'salary':'AED 150,000 - 200,000','salary_min':150000,'salary_max':200000,'skills':['SAP','Oracle','ERP','SQL'],'company':'Consulting Firms','experience':'4-7 yrs','type':'Full-time','growth':4,'score':52,'category':['risky'],'tags':['Warning'],'posted_days_ago':9},
        {'id':10,'role':'Site Reliability Engineer','openings':52,'salary':'AED 190,000 - 280,000','salary_min':190000,'salary_max':280000,'skills':['Linux','AWS','Python','Monitoring'],'company':'Various','experience':'4-6 yrs','type':'Full-time','growth':9,'score':88,'category':['emergency','new'],'tags':['Alarm','New'],'posted_days_ago':1},
    ],
    'tokyo': [
        {'id':1,'role':'C++ Developer','openings':280,'salary':'\u00a56,000,000 - 9,000,000','salary_min':6000000,'salary_max':9000000,'skills':['C++','Python','Linux','Embedded'],'company':'Sony/Toyota Tech','experience':'3-6 yrs','type':'Full-time','growth':7,'score':78,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':4},
        {'id':2,'role':'Game Developer','openings':350,'salary':'\u00a55,500,000 - 8,500,000','salary_min':5500000,'salary_max':8500000,'skills':['Unity','C#','Game Development','Graphics'],'company':'Gaming Studios','experience':'2-5 yrs','type':'Full-time','growth':7,'score':76,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':2},
        {'id':3,'role':'Web Developer','openings':320,'salary':'\u00a54,500,000 - 7,000,000','salary_min':4500000,'salary_max':7000000,'skills':['JavaScript','React','Node.js','CSS'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':6,'score':68,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':3},
        {'id':4,'role':'QA Tester','openings':200,'salary':'\u00a53,000,000 - 5,000,000','salary_min':3000000,'salary_max':5000000,'skills':['Testing','Selenium','Automation','Manual QA'],'company':'Various','experience':'1-3 yrs','type':'Full-time','growth':3,'score':40,'category':['risky'],'tags':['Warning'],'posted_days_ago':10},
        {'id':5,'role':'Embedded Systems Engineer','openings':52,'salary':'\u00a57,000,000 - 11,000,000','salary_min':7000000,'salary_max':11000000,'skills':['Embedded','C++','FPGA','IoT'],'company':'Manufacturing','experience':'4-7 yrs','type':'Full-time','growth':6,'score':72,'category':['emergency','high_pay'],'tags':['Alarm','Money'],'posted_days_ago':5},
        {'id':6,'role':'AI Engineer','openings':180,'salary':'\u00a58,000,000 - 12,000,000','salary_min':8000000,'salary_max':12000000,'skills':['Python','TensorFlow','PyTorch','NLP'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':10,'score':94,'category':['high_pay','best','new'],'tags':['Money','Star','New'],'posted_days_ago':2},
        {'id':7,'role':'Mainframe Operator','openings':30,'salary':'\u00a54,000,000 - 6,000,000','salary_min':4000000,'salary_max':6000000,'skills':['Mainframe','COBOL','JCL','MVS'],'company':'Banks','experience':'5+ yrs','type':'Full-time','growth':1,'score':20,'category':['risky'],'tags':['Warning'],'posted_days_ago':15},
        {'id':8,'role':'Cloud Engineer','openings':240,'salary':'\u00a57,000,000 - 11,000,000','salary_min':7000000,'salary_max':11000000,'skills':['AWS','Azure','Kubernetes','Terraform'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':87,'category':['high_demand','high_pay','best'],'tags':['Fire','Money','Star'],'posted_days_ago':3},
        {'id':9,'role':'Cybersecurity Specialist','openings':55,'salary':'\u00a58,000,000 - 12,000,000','salary_min':8000000,'salary_max':12000000,'skills':['Cybersecurity','Network','Penetration Testing'],'company':'Various','experience':'4-6 yrs','type':'Full-time','growth':9,'score':90,'category':['emergency','high_pay'],'tags':['Alarm','Money'],'posted_days_ago':1},
        {'id':10,'role':'React Developer','openings':260,'salary':'\u00a55,500,000 - 8,500,000','salary_min':5500000,'salary_max':8500000,'skills':['React','TypeScript','JavaScript','CSS'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':7,'score':75,'category':['high_demand','new'],'tags':['Fire','New'],'posted_days_ago':1},
    ],
    'sydney': [
        {'id':1,'role':'Solutions Architect','openings':240,'salary':'AUD 140,000 - 190,000','salary_min':140000,'salary_max':190000,'skills':['AWS','Azure','Enterprise','Solutions'],'company':'Various','experience':'6-9 yrs','type':'Full-time','growth':8,'score':85,'category':['high_pay','best'],'tags':['Money','Star'],'posted_days_ago':3},
        {'id':2,'role':'Senior Python Developer','openings':290,'salary':'AUD 130,000 - 180,000','salary_min':130000,'salary_max':180000,'skills':['Python','Django','PostgreSQL','AWS'],'company':'Various','experience':'4-6 yrs','type':'Full-time','growth':8,'score':84,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':2},
        {'id':3,'role':'Mobile Developer','openings':210,'salary':'AUD 100,000 - 150,000','salary_min':100000,'salary_max':150000,'skills':['React Native','Swift','Kotlin','Mobile'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':7,'score':77,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':5},
        {'id':4,'role':'Junior Developer','openings':180,'salary':'AUD 70,000 - 100,000','salary_min':70000,'salary_max':100000,'skills':['JavaScript','Python','Basics','Git'],'company':'Various','experience':'0-2 yrs','type':'Full-time','growth':7,'score':65,'category':['new'],'tags':['New'],'posted_days_ago':1},
        {'id':5,'role':'Data Engineer','openings':52,'salary':'AUD 130,000 - 175,000','salary_min':130000,'salary_max':175000,'skills':['Spark','Python','SQL','Airflow'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':88,'category':['emergency','high_pay'],'tags':['Alarm','Money'],'posted_days_ago':2},
        {'id':6,'role':'Cybersecurity Analyst','openings':56,'salary':'AUD 110,000 - 155,000','salary_min':110000,'salary_max':155000,'skills':['Cybersecurity','SIEM','Network','Linux'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':9,'score':88,'category':['emergency','new'],'tags':['Alarm','New'],'posted_days_ago':3},
        {'id':7,'role':'Legacy Oracle DBA','openings':80,'salary':'AUD 100,000 - 140,000','salary_min':100000,'salary_max':140000,'skills':['Oracle','SQL','DBA','Tuning'],'company':'Enterprise','experience':'5+ yrs','type':'Full-time','growth':2,'score':30,'category':['risky'],'tags':['Warning'],'posted_days_ago':14},
        {'id':8,'role':'ML Engineer','openings':160,'salary':'AUD 130,000 - 180,000','salary_min':130000,'salary_max':180000,'skills':['Python','TensorFlow','Scikit-learn','NLP'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':10,'score':93,'category':['high_pay','best','new'],'tags':['Money','Star','New'],'posted_days_ago':2},
        {'id':9,'role':'DevOps Engineer','openings':200,'salary':'AUD 120,000 - 160,000','salary_min':120000,'salary_max':160000,'skills':['Docker','Kubernetes','AWS','Terraform'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':8,'score':83,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':4},
        {'id':10,'role':'Full Stack Developer','openings':230,'salary':'AUD 110,000 - 155,000','salary_min':110000,'salary_max':155000,'skills':['React','Node.js','MongoDB','AWS'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':8,'score':80,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':3},
    ],
    'toronto': [
        {'id':1,'role':'Machine Learning Engineer','openings':270,'salary':'CAD 120,000 - 170,000','salary_min':120000,'salary_max':170000,'skills':['Python','TensorFlow','PyTorch','Data Science'],'company':'Vector Institute area','experience':'3-5 yrs','type':'Full-time','growth':10,'score':93,'category':['high_demand','high_pay','best'],'tags':['Fire','Money','Star'],'posted_days_ago':2},
        {'id':2,'role':'DevOps Engineer','openings':250,'salary':'CAD 110,000 - 160,000','salary_min':110000,'salary_max':160000,'skills':['Kubernetes','Docker','Terraform','AWS'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':8,'score':84,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':3},
        {'id':3,'role':'Backend Developer','openings':320,'salary':'CAD 90,000 - 140,000','salary_min':90000,'salary_max':140000,'skills':['Java','Python','Node.js','REST API'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':7,'score':76,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':4},
        {'id':4,'role':'Systems Administrator','openings':180,'salary':'CAD 70,000 - 110,000','salary_min':70000,'salary_max':110000,'skills':['Linux','Windows','Networking','Security'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':3,'score':42,'category':['risky'],'tags':['Warning'],'posted_days_ago':9},
        {'id':5,'role':'Cybersecurity Specialist','openings':53,'salary':'CAD 115,000 - 160,000','salary_min':115000,'salary_max':160000,'skills':['Cybersecurity','SIEM','Network','Penetration Testing'],'company':'Various','experience':'4-6 yrs','type':'Full-time','growth':9,'score':90,'category':['emergency','high_pay'],'tags':['Alarm','Money'],'posted_days_ago':1},
        {'id':6,'role':'Data Scientist','openings':210,'salary':'CAD 100,000 - 150,000','salary_min':100000,'salary_max':150000,'skills':['Python','R','Machine Learning','SQL'],'company':'Various','experience':'2-5 yrs','type':'Full-time','growth':9,'score':88,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':2},
        {'id':7,'role':'Cloud Architect','openings':180,'salary':'CAD 130,000 - 180,000','salary_min':130000,'salary_max':180000,'skills':['AWS','Azure','GCP','Terraform'],'company':'Various','experience':'5-8 yrs','type':'Full-time','growth':9,'score':90,'category':['high_pay','best'],'tags':['Money','Star'],'posted_days_ago':3},
        {'id':8,'role':'QA Automation Engineer','openings':130,'salary':'CAD 80,000 - 120,000','salary_min':80000,'salary_max':120000,'skills':['Selenium','Python','Cypress','Jest'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':4,'score':52,'category':['risky'],'tags':['Warning'],'posted_days_ago':11},
        {'id':9,'role':'React Developer','openings':240,'salary':'CAD 90,000 - 130,000','salary_min':90000,'salary_max':130000,'skills':['React','TypeScript','JavaScript','Redux'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':7,'score':76,'category':['high_demand','new'],'tags':['Fire','New'],'posted_days_ago':1},
        {'id':10,'role':'Blockchain Developer','openings':52,'salary':'CAD 120,000 - 170,000','salary_min':120000,'salary_max':170000,'skills':['Blockchain','Solidity','Web3','Ethereum'],'company':'FinTech','experience':'2-4 yrs','type':'Full-time','growth':6,'score':68,'category':['emergency','new'],'tags':['Alarm','New'],'posted_days_ago':2},
    ],
    'vizag': [
        {'id':1,'role':'Software Engineer','openings':380,'salary':'\u20b98,00,000 - \u20b912,00,000','salary_min':800000,'salary_max':1200000,'skills':['Python','Java','JavaScript','SQL'],'company':'HPCL/Steel Plant IT','experience':'2-4 yrs','type':'Full-time','growth':7,'score':75,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':3},
        {'id':2,'role':'Frontend Developer','openings':290,'salary':'\u20b97,00,000 - \u20b911,00,000','salary_min':700000,'salary_max':1100000,'skills':['React','HTML','CSS','JavaScript'],'company':'Various','experience':'1-3 yrs','type':'Full-time','growth':7,'score':72,'category':['high_demand'],'tags':['Fire'],'posted_days_ago':2},
        {'id':3,'role':'Data Engineer','openings':250,'salary':'\u20b99,00,000 - \u20b913,00,000','salary_min':900000,'salary_max':1300000,'skills':['Python','Spark','SQL','Hadoop'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':9,'score':85,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':4},
        {'id':4,'role':'Full Stack Developer','openings':320,'salary':'\u20b98,50,000 - \u20b912,50,000','salary_min':850000,'salary_max':1250000,'skills':['React','Node.js','MongoDB','Express'],'company':'Various','experience':'2-4 yrs','type':'Full-time','growth':8,'score':80,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':1},
        {'id':5,'role':'DevOps Engineer','openings':180,'salary':'\u20b99,00,000 - \u20b913,00,000','salary_min':900000,'salary_max':1300000,'skills':['Docker','Kubernetes','AWS','Linux'],'company':'Various','experience':'3-5 yrs','type':'Full-time','growth':8,'score':82,'category':['high_demand','best'],'tags':['Fire','Star'],'posted_days_ago':5},
        {'id':6,'role':'QA Engineer','openings':150,'salary':'\u20b95,00,000 - \u20b98,00,000','salary_min':500000,'salary_max':800000,'skills':['Selenium','Testing','Automation','Manual QA'],'company':'Various','experience':'1-3 yrs','type':'Full-time','growth':3,'score':40,'category':['risky'],'tags':['Warning'],'posted_days_ago':12},
        {'id':7,'role':'ML Engineer','openings':55,'salary':'\u20b912,00,000 - \u20b918,00,000','salary_min':1200000,'salary_max':1800000,'skills':['Python','TensorFlow','Data Science','NLP'],'company':'IT Parks','experience':'2-5 yrs','type':'Full-time','growth':10,'score':92,'category':['high_pay','best','emergency'],'tags':['Money','Star','Alarm'],'posted_days_ago':2},
        {'id':8,'role':'Data Entry Operator','openings':120,'salary':'\u20b93,00,000 - \u20b94,50,000','salary_min':300000,'salary_max':450000,'skills':['Excel','Typing','MS Office','Data Entry'],'company':'BPO','experience':'0-1 yr','type':'Full-time','growth':1,'score':15,'category':['risky'],'tags':['Warning'],'posted_days_ago':20},
        {'id':9,'role':'Cybersecurity Analyst','openings':52,'salary':'\u20b910,00,000 - \u20b915,00,000','salary_min':1000000,'salary_max':1500000,'skills':['Cybersecurity','Linux','Network','VAPT'],'company':'Defence/Govt IT','experience':'3-5 yrs','type':'Full-time','growth':9,'score':88,'category':['emergency','new'],'tags':['Alarm','New'],'posted_days_ago':1},
        {'id':10,'role':'Cloud Engineer','openings':150,'salary':'\u20b910,00,000 - \u20b915,00,000','salary_min':1000000,'salary_max':1500000,'skills':['AWS','Azure','Docker','Kubernetes'],'company':'IT Parks','experience':'2-4 yrs','type':'Full-time','growth':9,'score':86,'category':['high_demand','new','best'],'tags':['Fire','New','Star'],'posted_days_ago':3},
    ],
}

COMPANIES_DATA = {
    'new york': [
        {'name':'JPMorgan Chase','rating':4.2,'openings':320,'salary':'$110,000 - $180,000','skills':['Java','Python','SQL','Finance'],'benefits':'Health, 401k, Bonus','growth':'High'},
        {'name':'Goldman Sachs','rating':4.1,'openings':210,'salary':'$120,000 - $200,000','skills':['Python','Quant','SQL','C++'],'benefits':'Top bonus, Health','growth':'High'},
        {'name':'Citigroup','rating':3.9,'openings':280,'salary':'$100,000 - $160,000','skills':['Java','SQL','FinTech','APIs'],'benefits':'Health, Pension','growth':'Medium'},
        {'name':'Bloomberg','rating':4.5,'openings':150,'salary':'$130,000 - $190,000','skills':['C++','Python','Financial Data'],'benefits':'Best in class','growth':'High'},
        {'name':'Google NYC','rating':4.8,'openings':200,'salary':'$150,000 - $250,000','skills':['Python','Go','ML','Kubernetes'],'benefits':'Legendary perks','growth':'Very High'},
        {'name':'Amazon AWS NY','rating':4.3,'openings':180,'salary':'$140,000 - $230,000','skills':['AWS','Java','Python','Distributed'],'benefits':'RSU, Health','growth':'Very High'},
        {'name':'Microsoft NY','rating':4.4,'openings':160,'salary':'$130,000 - $210,000','skills':['C#','.NET','Azure','Python'],'benefits':'Stock, Health','growth':'High'},
        {'name':'Meta NY','rating':4.5,'openings':140,'salary':'$150,000 - $250,000','skills':['React','Python','ML'],'benefits':'Top equity','growth':'High'},
        {'name':'IBM NY','rating':3.8,'openings':220,'salary':'$90,000 - $150,000','skills':['Java','Cloud','Watson','DevOps'],'benefits':'Health, Pension','growth':'Medium'},
        {'name':'Accenture NY','rating':3.9,'openings':300,'salary':'$80,000 - $140,000','skills':['Consulting','SAP','Java','Cloud'],'benefits':'Health, Travel','growth':'Medium'},
        {'name':'Palantir','rating':4.2,'openings':80,'salary':'$140,000 - $220,000','skills':['Python','Data','Analytics'],'benefits':'Equity, Health','growth':'High'},
        {'name':'Two Sigma','rating':4.6,'openings':60,'salary':'$150,000 - $300,000','skills':['Python','C++','Quant','ML'],'benefits':'Best bonus','growth':'Very High'},
    ],
    'bangalore': [
        {'name':'Infosys','rating':3.8,'openings':2000,'salary':'\u20b98,00,000 - \u20b920,00,000','skills':['Java','SAP','Python','Cloud'],'benefits':'Health, Training','growth':'Medium'},
        {'name':'Wipro','rating':3.7,'openings':1800,'salary':'\u20b97,00,000 - \u20b918,00,000','skills':['Java','Testing','Cloud','SAP'],'benefits':'Health, Flexi','growth':'Medium'},
        {'name':'TCS','rating':3.9,'openings':3000,'salary':'\u20b96,00,000 - \u20b920,00,000','skills':['Java','Python','Cloud','Testing'],'benefits':'Health, PF','growth':'Medium'},
        {'name':'Google India','rating':4.9,'openings':400,'salary':'\u20b925,00,000 - \u20b980,00,000','skills':['Python','Go','ML','SRE'],'benefits':'World class','growth':'Very High'},
        {'name':'Amazon India','rating':4.4,'openings':600,'salary':'\u20b920,00,000 - \u20b960,00,000','skills':['Java','Python','AWS','ML'],'benefits':'RSU, Health','growth':'Very High'},
        {'name':'Microsoft IDC','rating':4.5,'openings':350,'salary':'\u20b922,00,000 - \u20b965,00,000','skills':['C#','Azure','.NET','Python'],'benefits':'ESOP, Health','growth':'High'},
        {'name':'Flipkart','rating':4.3,'openings':400,'salary':'\u20b918,00,000 - \u20b950,00,000','skills':['Java','Python','Spark','ML'],'benefits':'ESOPs, Health','growth':'High'},
        {'name':'Swiggy','rating':4.2,'openings':250,'salary':'\u20b915,00,000 - \u20b940,00,000','skills':['Python','Go','React','ML'],'benefits':'Free food, ESOP','growth':'High'},
        {'name':'PhonePe','rating':4.3,'openings':200,'salary':'\u20b918,00,000 - \u20b950,00,000','skills':['Java','Python','Payments','ML'],'benefits':'ESOP, Health','growth':'High'},
        {'name':'Razorpay','rating':4.4,'openings':180,'salary':'\u20b920,00,000 - \u20b955,00,000','skills':['Java','Go','FinTech','APIs'],'benefits':'ESOP, Remote','growth':'Very High'},
        {'name':'CRED','rating':4.2,'openings':120,'salary':'\u20b922,00,000 - \u20b960,00,000','skills':['Python','ML','React','Data'],'benefits':'ESOP, Remote','growth':'High'},
        {'name':'Zepto','rating':4.1,'openings':150,'salary':'\u20b918,00,000 - \u20b945,00,000','skills':['Python','React','ML','Data'],'benefits':'ESOP, Health','growth':'Very High'},
    ],
    'london': [
        {'name':'HSBC Tech','rating':3.9,'openings':400,'salary':'\u00a365,000 - \u00a3120,000','skills':['Java','Python','FinTech','Cloud'],'benefits':'Pension, Health','growth':'Medium'},
        {'name':'Barclays Tech','rating':4.0,'openings':350,'salary':'\u00a370,000 - \u00a3130,000','skills':['Java','Python','Cloud','APIs'],'benefits':'Bonus, Pension','growth':'Medium'},
        {'name':'Revolut','rating':4.2,'openings':300,'salary':'\u00a380,000 - \u00a3160,000','skills':['Python','Go','FinTech','ML'],'benefits':'ESOP, Remote','growth':'Very High'},
        {'name':'Monzo','rating':4.4,'openings':200,'salary':'\u00a375,000 - \u00a3150,000','skills':['Go','Python','React','Banking'],'benefits':'ESOP, Flexi','growth':'High'},
        {'name':'DeepMind','rating':4.8,'openings':100,'salary':'\u00a390,000 - \u00a3200,000','skills':['Python','ML','Research','TensorFlow'],'benefits':'Best in AI','growth':'Very High'},
        {'name':'Google London','rating':4.7,'openings':250,'salary':'\u00a3100,000 - \u00a3200,000','skills':['Python','Go','ML','SRE'],'benefits':'Legendary','growth':'Very High'},
        {'name':'Amazon London','rating':4.3,'openings':300,'salary':'\u00a385,000 - \u00a3180,000','skills':['Java','Python','AWS','ML'],'benefits':'RSU, Health','growth':'Very High'},
        {'name':'Sky Tech','rating':3.9,'openings':200,'salary':'\u00a355,000 - \u00a3100,000','skills':['Java','Python','Media','Cloud'],'benefits':'TV, Health','growth':'Medium'},
        {'name':'Checkout.com','rating':4.3,'openings':150,'salary':'\u00a380,000 - \u00a3160,000','skills':['Go','Python','Payments','APIs'],'benefits':'ESOP, Flexi','growth':'Very High'},
        {'name':'Wise','rating':4.4,'openings':180,'salary':'\u00a375,000 - \u00a3150,000','skills':['Python','Go','FinTech','Data'],'benefits':'ESOP, Remote','growth':'High'},
        {'name':'Arm Holdings','rating':4.3,'openings':200,'salary':'\u00a370,000 - \u00a3140,000','skills':['C++','Embedded','ARM','VLSI'],'benefits':'ESOP, Pension','growth':'High'},
        {'name':'Babylon Health','rating':4.0,'openings':120,'salary':'\u00a370,000 - \u00a3130,000','skills':['Python','ML','Health Tech'],'benefits':'Health, Equity','growth':'High'},
    ],
    'dubai': [
        {'name':'Emirates Group IT','rating':4.2,'openings':300,'salary':'AED 150,000 - 250,000','skills':['Java','SAP','Cloud','APIs'],'benefits':'Housing, Health','growth':'High'},
        {'name':'ENOC Tech','rating':3.9,'openings':200,'salary':'AED 140,000 - 220,000','skills':['SAP','Python','Data','Cloud'],'benefits':'Housing, Medical','growth':'Medium'},
        {'name':'DIFC FinTech','rating':4.3,'openings':150,'salary':'AED 180,000 - 300,000','skills':['Python','FinTech','Blockchain','ML'],'benefits':'Housing, Bonus','growth':'Very High'},
        {'name':'Careem','rating':4.4,'openings':250,'salary':'AED 150,000 - 250,000','skills':['Python','Go','React','ML'],'benefits':'ESOP, Remote','growth':'High'},
        {'name':'Noon.com','rating':4.0,'openings':200,'salary':'AED 140,000 - 230,000','skills':['Java','Python','E-commerce','ML'],'benefits':'Housing, Health','growth':'High'},
        {'name':'Property Finder','rating':4.2,'openings':120,'salary':'AED 140,000 - 220,000','skills':['React','Node.js','Python','Data'],'benefits':'ESOP, Remote','growth':'High'},
        {'name':'Mashreq Bank Tech','rating':3.9,'openings':180,'salary':'AED 150,000 - 250,000','skills':['Java','Python','Banking','APIs'],'benefits':'Medical, Housing','growth':'Medium'},
        {'name':'du Telecom','rating':3.8,'openings':150,'salary':'AED 130,000 - 210,000','skills':['Telecom','Python','Cloud','5G'],'benefits':'Medical, Housing','growth':'Medium'},
        {'name':'Abu Dhabi Gov Tech','rating':4.0,'openings':250,'salary':'AED 160,000 - 260,000','skills':['Cloud','Python','Gov Tech','Security'],'benefits':'Housing, Pension','growth':'Medium'},
        {'name':'Dubizzle','rating':3.8,'openings':100,'salary':'AED 120,000 - 200,000','skills':['Python','React','Mobile','APIs'],'benefits':'Health, Flexi','growth':'Medium'},
    ],
    'tokyo': [
        {'name':'Sony Digital','rating':4.3,'openings':300,'salary':'\u00a56,000,000 - 12,000,000','skills':['C++','Python','Embedded','DSP'],'benefits':'Pension, Health','growth':'High'},
        {'name':'Toyota Tech','rating':4.2,'openings':400,'salary':'\u00a56,500,000 - 11,000,000','skills':['C++','Embedded','AI','Automotive'],'benefits':'Housing, Pension','growth':'High'},
        {'name':'Rakuten','rating':4.0,'openings':350,'salary':'\u00a55,500,000 - 10,000,000','skills':['Java','Python','E-commerce','ML'],'benefits':'Discount, Health','growth':'Medium'},
        {'name':'SoftBank Tech','rating':3.9,'openings':280,'salary':'\u00a56,000,000 - 10,000,000','skills':['Python','AI','Cloud','5G'],'benefits':'Phone, Health','growth':'Medium'},
        {'name':'LINE Corp','rating':4.3,'openings':200,'salary':'\u00a56,500,000 - 12,000,000','skills':['Java','Go','React','ML'],'benefits':'ESOP, Remote','growth':'High'},
        {'name':'Mercari','rating':4.4,'openings':150,'salary':'\u00a57,000,000 - 14,000,000','skills':['Go','Python','ML','React'],'benefits':'ESOP, Remote','growth':'Very High'},
        {'name':'CyberAgent','rating':4.2,'openings':180,'salary':'\u00a55,500,000 - 10,000,000','skills':['Python','Java','ML','Gaming'],'benefits':'Game perks, Health','growth':'High'},
        {'name':'Nintendo','rating':4.6,'openings':120,'salary':'\u00a57,000,000 - 13,000,000','skills':['C++','Game Dev','Graphics','Unity'],'benefits':'Best gaming','growth':'High'},
        {'name':'Capcom','rating':4.4,'openings':100,'salary':'\u00a55,500,000 - 10,000,000','skills':['C++','Unity','Game Dev','Graphics'],'benefits':'Game perks','growth':'Medium'},
        {'name':'Fujitsu','rating':3.8,'openings':400,'salary':'\u00a55,000,000 - 9,000,000','skills':['Java','Cloud','SAP','IT Services'],'benefits':'Pension, Health','growth':'Low'},
    ],
    'sydney': [
        {'name':'Atlassian','rating':4.7,'openings':300,'salary':'AUD 130,000 - 220,000','skills':['Java','Python','React','Cloud'],'benefits':'Best in class','growth':'Very High'},
        {'name':'Canva','rating':4.8,'openings':250,'salary':'AUD 140,000 - 230,000','skills':['Python','React','Design','ML'],'benefits':'Equity, Remote','growth':'Very High'},
        {'name':'Afterpay','rating':4.3,'openings':150,'salary':'AUD 120,000 - 200,000','skills':['Java','Python','FinTech','Mobile'],'benefits':'ESOP, Flexi','growth':'High'},
        {'name':'Commonwealth Bank Tech','rating':3.9,'openings':400,'salary':'AUD 100,000 - 175,000','skills':['Java','Python','Banking','Cloud'],'benefits':'Pension, Health','growth':'Medium'},
        {'name':'Telstra Tech','rating':3.8,'openings':300,'salary':'AUD 95,000 - 160,000','skills':['Python','Java','Telecom','5G'],'benefits':'Phone, Health','growth':'Medium'},
        {'name':'REA Group','rating':4.4,'openings':150,'salary':'AUD 120,000 - 200,000','skills':['Kotlin','Swift','React','AWS'],'benefits':'ESOP, Flexi','growth':'High'},
        {'name':'WiseTech Global','rating':4.3,'openings':120,'salary':'AUD 115,000 - 190,000','skills':['Java','React','Logistics','Cloud'],'benefits':'ESOP, Bonus','growth':'High'},
        {'name':'Xero','rating':4.5,'openings':180,'salary':'AUD 110,000 - 180,000','skills':['Python','React','Cloud','SaaS'],'benefits':'ESOP, Remote','growth':'Very High'},
        {'name':'SEEK','rating':4.3,'openings':140,'salary':'AUD 110,000 - 185,000','skills':['Python','React','ML','Data'],'benefits':'ESOP, Health','growth':'High'},
        {'name':'Macquarie Group Tech','rating':4.1,'openings':200,'salary':'AUD 120,000 - 200,000','skills':['Python','Java','Finance','ML'],'benefits':'Bonus, Health','growth':'High'},
    ],
    'toronto': [
        {'name':'Shopify','rating':4.7,'openings':400,'salary':'CAD 130,000 - 220,000','skills':['Ruby','Python','React','Cloud'],'benefits':'Remote first','growth':'Very High'},
        {'name':'RBC Tech','rating':4.0,'openings':500,'salary':'CAD 95,000 - 165,000','skills':['Java','Python','Banking','Cloud'],'benefits':'Pension, Health','growth':'Medium'},
        {'name':'TD Bank Tech','rating':3.9,'openings':450,'salary':'CAD 90,000 - 155,000','skills':['Java','Python','SQL','FinTech'],'benefits':'Pension, Bonus','growth':'Medium'},
        {'name':'Hootsuite','rating':4.2,'openings':100,'salary':'CAD 95,000 - 160,000','skills':['Python','React','Social Media','Data'],'benefits':'Remote, Health','growth':'Medium'},
        {'name':'Coveo','rating':4.4,'openings':120,'salary':'CAD 100,000 - 175,000','skills':['Python','ML','Search','Cloud'],'benefits':'ESOP, Remote','growth':'High'},
        {'name':'D2L','rating':4.2,'openings':90,'salary':'CAD 90,000 - 155,000','skills':['Python','React','EdTech','Cloud'],'benefits':'Remote, Health','growth':'High'},
        {'name':'PointClickCare','rating':4.3,'openings':130,'salary':'CAD 95,000 - 165,000','skills':['Java','Python','Health Tech','Cloud'],'benefits':'ESOP, Health','growth':'High'},
        {'name':'Ubisoft Toronto','rating':4.2,'openings':150,'salary':'CAD 80,000 - 150,000','skills':['C++','Game Dev','Unity','Graphics'],'benefits':'Game perks','growth':'Medium'},
        {'name':'BlackBerry Tech','rating':3.7,'openings':200,'salary':'CAD 90,000 - 155,000','skills':['C++','Security','Embedded','IoT'],'benefits':'Health, Pension','growth':'Low'},
        {'name':'Wattpad','rating':4.3,'openings':80,'salary':'CAD 100,000 - 170,000','skills':['Python','React','ML','Content'],'benefits':'Remote, ESOP','growth':'High'},
    ],
    'vizag': [
        {'name':'Wipro Vizag','rating':3.7,'openings':300,'salary':'\u20b96,00,000 - \u20b914,00,000','skills':['Java','Testing','SAP','Cloud'],'benefits':'Health, Training','growth':'Medium'},
        {'name':'TCS Vizag','rating':3.8,'openings':400,'salary':'\u20b95,00,000 - \u20b915,00,000','skills':['Java','Python','Testing','SAP'],'benefits':'Health, PF','growth':'Medium'},
        {'name':'HPCL IT','rating':3.9,'openings':150,'salary':'\u20b910,00,000 - \u20b918,00,000','skills':['SAP','Python','ERPs','Data'],'benefits':'Housing, PF','growth':'Medium'},
        {'name':'Steel Authority IT','rating':3.8,'openings':120,'salary':'\u20b98,00,000 - \u20b916,00,000','skills':['SAP','ERPs','Java','Data'],'benefits':'Housing, Pension','growth':'Low'},
        {'name':'RINL Tech','rating':3.7,'openings':80,'salary':'\u20b97,00,000 - \u20b914,00,000','skills':['Java','SAP','Networks','IT Support'],'benefits':'Housing, Medical','growth':'Low'},
        {'name':'Vizag IT Park MNCs','rating':4.0,'openings':500,'salary':'\u20b98,00,000 - \u20b920,00,000','skills':['Python','Java','React','Cloud'],'benefits':'Health, WFH','growth':'High'},
        {'name':'Zoho Vizag','rating':4.4,'openings':200,'salary':'\u20b99,00,000 - \u20b918,00,000','skills':['Java','Python','SaaS','Cloud'],'benefits':'Best culture','growth':'High'},
        {'name':'ECIL','rating':3.6,'openings':100,'salary':'\u20b97,00,000 - \u20b913,00,000','skills':['Embedded','C','Linux','Defence'],'benefits':'Govt benefits','growth':'Low'},
        {'name':'IndiaMart Vizag','rating':3.8,'openings':80,'salary':'\u20b96,00,000 - \u20b912,00,000','skills':['Java','React','APIs','Data'],'benefits':'Health, Flexi','growth':'Medium'},
        {'name':'BSNL IT Vizag','rating':3.3,'openings':50,'salary':'\u20b95,00,000 - \u20b910,00,000','skills':['Networks','Linux','Telecom'],'benefits':'Govt benefits','growth':'Very Low'},
    ],
}

STARTUPS_DATA = {
    'new york': [
        {'name':'DataForge AI','stage':'Series B','roles':['ML Engineer','Data Scientist'],'equity':'0.1-0.3%','salary':'$100,000-$145,000','growth':9,'description':'AI-powered data analytics platform'},
        {'name':'UrbanFlow','stage':'Series A','roles':['Backend Dev','DevOps'],'equity':'0.2-0.5%','salary':'$90,000-$130,000','growth':8,'description':'Smart city mobility solutions'},
        {'name':'HealthAI','stage':'Series C','roles':['ML Engineer','Full Stack'],'equity':'0.05-0.15%','salary':'$110,000-$155,000','growth':9,'description':'AI diagnostics for hospitals'},
        {'name':'FinNova','stage':'Seed','roles':['Python Dev','React Dev'],'equity':'0.5-1.5%','salary':'$80,000-$120,000','growth':7,'description':'Next-gen digital banking'},
        {'name':'LegalTech Pro','stage':'Series A','roles':['NLP Engineer','Full Stack'],'equity':'0.3-0.8%','salary':'$95,000-$135,000','growth':8,'description':'AI-powered legal document processing'},
        {'name':'RetailX','stage':'Seed','roles':['React Dev','Mobile Dev'],'equity':'1.0-2.5%','salary':'$75,000-$110,000','growth':7,'description':'Omnichannel retail platform'},
    ],
    'bangalore': [
        {'name':'Sarvam AI','stage':'Series A','roles':['ML Engineer','NLP Researcher'],'equity':'0.3-0.8%','salary':'\u20b920,00,000-\u20b935,00,000','growth':10,'description':'Indian language AI models'},
        {'name':'Ather Energy','stage':'Series D','roles':['Embedded','Backend','ML'],'equity':'0.05-0.2%','salary':'\u20b918,00,000-\u20b932,00,000','growth':9,'description':'Electric vehicle tech'},
        {'name':'Unacademy','stage':'Series F','roles':['Full Stack','Mobile','ML'],'equity':'0.01-0.1%','salary':'\u20b915,00,000-\u20b928,00,000','growth':7,'description':'EdTech platform'},
        {'name':'GrowthX','stage':'Seed','roles':['React Dev','Backend'],'equity':'0.8-2%','salary':'\u20b912,00,000-\u20b922,00,000','growth':8,'description':'B2B growth analytics'},
        {'name':'Mintifi','stage':'Series B','roles':['Java Dev','Data Engineer'],'equity':'0.2-0.5%','salary':'\u20b918,00,000-\u20b928,00,000','growth':9,'description':'Supply chain financing'},
        {'name':'BrowserStack','stage':'Series B','roles':['Full Stack','QA','DevOps'],'equity':'0.1-0.3%','salary':'\u20b918,00,000-\u20b932,00,000','growth':8,'description':'Cloud browser testing platform'},
    ],
    'london': [
        {'name':'Synthesia','stage':'Series C','roles':['ML Engineer','Video AI','Full Stack'],'equity':'0.05-0.15%','salary':'\u00a380,000-\u00a3130,000','growth':10,'description':'AI video generation'},
        {'name':'Tractable','stage':'Series D','roles':['ML Engineer','Data Scientist'],'equity':'0.05-0.2%','salary':'\u00a375,000-\u00a3120,000','growth':9,'description':'AI for insurance claims'},
        {'name':'Wayve','stage':'Series B','roles':['ML Engineer','C++','Robotics'],'equity':'0.1-0.4%','salary':'\u00a380,000-\u00a3130,000','growth':10,'description':'Autonomous driving AI'},
        {'name':'Thought Machine','stage':'Series D','roles':['Java Dev','Cloud Eng','SRE'],'equity':'0.05-0.2%','salary':'\u00a370,000-\u00a3120,000','growth':9,'description':'Cloud-native core banking'},
        {'name':'Featurespace','stage':'Series E','roles':['ML Engineer','Data Scientist'],'equity':'0.05-0.15%','salary':'\u00a370,000-\u00a3115,000','growth':8,'description':'Real-time ML for fraud prevention'},
        {'name':'Quantexa','stage':'Series E','roles':['Data Engineer','ML','Backend'],'equity':'0.05-0.2%','salary':'\u00a375,000-\u00a3120,000','growth':9,'description':'Decision intelligence platform'},
    ],
    'dubai': [
        {'name':'Huspy','stage':'Series A','roles':['Full Stack','Mobile','ML'],'equity':'0.3-0.8%','salary':'AED 140,000-220,000','growth':9,'description':'Digital mortgage platform'},
        {'name':'Cafu','stage':'Series B','roles':['Backend','Mobile','DevOps'],'equity':'0.2-0.5%','salary':'AED 130,000-210,000','growth':8,'description':'On-demand fuel delivery app'},
        {'name':'Tamara','stage':'Series C','roles':['Java Dev','ML Engineer','Data'],'equity':'0.1-0.3%','salary':'AED 150,000-240,000','growth':9,'description':'BNPL fintech'},
        {'name':'Anghami','stage':'Public','roles':['Mobile Dev','Backend','ML'],'equity':'0.05-0.2%','salary':'AED 130,000-210,000','growth':7,'description':'Arab music streaming'},
        {'name':'Floward','stage':'Series B','roles':['Full Stack','Mobile'],'equity':'0.2-0.6%','salary':'AED 120,000-200,000','growth':8,'description':'Online flowers and gifts'},
        {'name':'Trukker','stage':'Series B','roles':['Backend','ML','Mobile'],'equity':'0.2-0.5%','salary':'AED 130,000-210,000','growth':8,'description':'Digital freight marketplace'},
    ],
    'tokyo': [
        {'name':'Preferred Networks','stage':'Series C','roles':['ML Engineer','C++ Dev','Research'],'equity':'0.1-0.4%','salary':'\u00a58,000,000-14,000,000','growth':10,'description':'Deep learning for robotics'},
        {'name':'SmartNews','stage':'Series F','roles':['ML Engineer','Data','Mobile'],'equity':'0.02-0.1%','salary':'\u00a57,000,000-12,000,000','growth':8,'description':'AI news discovery'},
        {'name':'Freee','stage':'Public','roles':['Java Dev','React','Mobile'],'equity':'0.01-0.1%','salary':'\u00a56,000,000-10,000,000','growth':8,'description':'Cloud accounting SaaS'},
        {'name':'Astroscale','stage':'Series F','roles':['Software Eng','Embedded','Systems'],'equity':'0.05-0.2%','salary':'\u00a57,000,000-12,000,000','growth':9,'description':'In-space debris removal'},
        {'name':'Tier IV','stage':'Series B','roles':['C++','ROS','Autonomous','ML'],'equity':'0.2-0.6%','salary':'\u00a58,000,000-14,000,000','growth':10,'description':'Open autonomous driving'},
        {'name':'Sansan','stage':'Public','roles':['ML Engineer','Full Stack','Data'],'equity':'0.01-0.1%','salary':'\u00a56,000,000-11,000,000','growth':7,'description':'AI business card and CRM'},
    ],
    'sydney': [
        {'name':'SafetyCulture','stage':'Series D','roles':['React','Node.js','Mobile','ML'],'equity':'0.05-0.2%','salary':'AUD 120,000-190,000','growth':9,'description':'Workplace safety platform'},
        {'name':'Immutable','stage':'Series C','roles':['Blockchain','Backend','ML'],'equity':'0.1-0.3%','salary':'AUD 130,000-200,000','growth':8,'description':'NFT gaming blockchain'},
        {'name':'Airtasker','stage':'Public','roles':['Full Stack','Mobile','ML'],'equity':'0.01-0.1%','salary':'AUD 100,000-165,000','growth':7,'description':'Task marketplace'},
        {'name':'Employment Hero','stage':'Series F','roles':['Full Stack','Data','ML'],'equity':'0.02-0.1%','salary':'AUD 110,000-175,000','growth':9,'description':'HR and payroll SaaS'},
        {'name':'Eucalyptus','stage':'Series C','roles':['Full Stack','Mobile','ML'],'equity':'0.1-0.4%','salary':'AUD 115,000-180,000','growth':9,'description':'Digital healthcare'},
        {'name':'Rokt','stage':'Series E','roles':['Full Stack','ML','Data'],'equity':'0.05-0.2%','salary':'AUD 120,000-190,000','growth':8,'description':'E-commerce ML platform'},
    ],
    'toronto': [
        {'name':'Cohere','stage':'Series C','roles':['ML Engineer','NLP Researcher','Full Stack'],'equity':'0.1-0.5%','salary':'CAD 130,000-220,000','growth':10,'description':'Enterprise NLP AI'},
        {'name':'Properly','stage':'Series B','roles':['Full Stack','ML','Data'],'equity':'0.2-0.6%','salary':'CAD 100,000-165,000','growth':8,'description':'AI-powered home buying'},
        {'name':'League','stage':'Series C','roles':['Full Stack','Mobile','Data'],'equity':'0.1-0.4%','salary':'CAD 100,000-165,000','growth':9,'description':'Health benefits platform'},
        {'name':'BenchSci','stage':'Series C','roles':['ML Engineer','Data','Full Stack'],'equity':'0.1-0.4%','salary':'CAD 105,000-170,000','growth':9,'description':'AI for biomedical research'},
        {'name':'Deep Genomics','stage':'Series B','roles':['ML Engineer','Bioinformatics'],'equity':'0.2-0.6%','salary':'CAD 105,000-170,000','growth':10,'description':'AI drug discovery'},
        {'name':'Nudge','stage':'Series A','roles':['Full Stack','Mobile'],'equity':'0.3-0.8%','salary':'CAD 90,000-145,000','growth':7,'description':'Financial wellness app'},
    ],
    'vizag': [
        {'name':'Vizag Tech Labs','stage':'Seed','roles':['Full Stack','React','Backend'],'equity':'1.0-3.0%','salary':'\u20b98,00,000-14,00,000','growth':7,'description':'Local tech solutions startup'},
        {'name':'GreenShip AI','stage':'Seed','roles':['Python Dev','ML','Data'],'equity':'1.5-4.0%','salary':'\u20b910,00,000-16,00,000','growth':8,'description':'AI for port logistics'},
        {'name':'AquaTech Vizag','stage':'Series A','roles':['IoT Dev','Backend','Mobile'],'equity':'0.5-1.5%','salary':'\u20b99,00,000-15,00,000','growth':8,'description':'Smart aquaculture monitoring'},
        {'name':'IndieAI','stage':'Seed','roles':['ML Engineer','NLP','Full Stack'],'equity':'2.0-5.0%','salary':'\u20b910,00,000-18,00,000','growth':9,'description':'AI-powered local language apps'},
        {'name':'SteelSmart','stage':'Series A','roles':['IoT','Embedded','Backend'],'equity':'0.8-2.0%','salary':'\u20b99,00,000-15,00,000','growth':7,'description':'Smart factory solutions for steel'},
        {'name':'FishTrack','stage':'Seed','roles':['Mobile Dev','Backend','IoT'],'equity':'2.0-5.0%','salary':'\u20b97,00,000-12,00,000','growth':7,'description':'Fishing boat logistics app'},
    ],
}

OFFICERS_DATA = {
    'new york': [
        {'name':'Sarah Johnson','specialization':'Tech & Software Engineering','success_rate':92,'phone':'+1-212-555-0101','email':'sarah.johnson@nyworkforce.com','experience':12,'placed':2400},
        {'name':'Michael Chen','specialization':'Finance & FinTech','success_rate':88,'phone':'+1-212-555-0102','email':'m.chen@nyworkforce.com','experience':9,'placed':1800},
        {'name':'Emily Rodriguez','specialization':'Data Science & AI/ML','success_rate':90,'phone':'+1-212-555-0103','email':'emily.r@nyworkforce.com','experience':7,'placed':1200},
        {'name':'David Park','specialization':'Cybersecurity & DevOps','success_rate':85,'phone':'+1-212-555-0104','email':'d.park@nyworkforce.com','experience':11,'placed':1600},
        {'name':'Lisa Thompson','specialization':'Product & UX','success_rate':87,'phone':'+1-212-555-0105','email':'l.thompson@nyworkforce.com','experience':8,'placed':980},
    ],
    'bangalore': [
        {'name':'Rajesh Kumar','specialization':'Full Stack & Backend Dev','success_rate':91,'phone':'+91-80-4567-0101','email':'rajesh.k@blrworkforce.com','experience':14,'placed':3200},
        {'name':'Priya Sharma','specialization':'ML/AI & Data Science','success_rate':93,'phone':'+91-80-4567-0102','email':'priya.s@blrworkforce.com','experience':8,'placed':1500},
        {'name':'Arun Nair','specialization':'DevOps & Cloud','success_rate':89,'phone':'+91-80-4567-0103','email':'arun.n@blrworkforce.com','experience':10,'placed':1800},
        {'name':'Deepika Reddy','specialization':'Product & Management','success_rate':86,'phone':'+91-80-4567-0104','email':'deepika.r@blrworkforce.com','experience':7,'placed':900},
        {'name':'Sanjay Mehta','specialization':'Mobile & Android/iOS','success_rate':88,'phone':'+91-80-4567-0105','email':'sanjay.m@blrworkforce.com','experience':9,'placed':1300},
    ],
    'london': [
        {'name':'James Wilson','specialization':'FinTech & Banking Tech','success_rate':90,'phone':'+44-20-7946-0101','email':'j.wilson@londonworkforce.com','experience':13,'placed':2100},
        {'name':'Sophie Brown','specialization':'AI/ML & Data Science','success_rate':92,'phone':'+44-20-7946-0102','email':'s.brown@londonworkforce.com','experience':8,'placed':1200},
        {'name':'Oliver Smith','specialization':'Full Stack & Backend','success_rate':88,'phone':'+44-20-7946-0103','email':'o.smith@londonworkforce.com','experience':10,'placed':1700},
        {'name':'Emma Davis','specialization':'Cybersecurity & Cloud','success_rate':89,'phone':'+44-20-7946-0104','email':'e.davis@londonworkforce.com','experience':9,'placed':1100},
        {'name':'Harry Taylor','specialization':'Gaming & Media Tech','success_rate':84,'phone':'+44-20-7946-0105','email':'h.taylor@londonworkforce.com','experience':7,'placed':750},
    ],
    'dubai': [
        {'name':'Ahmed Al-Rashid','specialization':'Cloud & Enterprise Tech','success_rate':88,'phone':'+971-4-555-0101','email':'ahmed.r@dubaiworkforce.com','experience':11,'placed':1600},
        {'name':'Fatima Al-Zaabi','specialization':'FinTech & Blockchain','success_rate':85,'phone':'+971-4-555-0102','email':'fatima.z@dubaiworkforce.com','experience':7,'placed':900},
        {'name':'Rohit Sharma','specialization':'Full Stack & Mobile','success_rate':90,'phone':'+971-4-555-0103','email':'rohit.s@dubaiworkforce.com','experience':9,'placed':1400},
        {'name':'Layla Hassan','specialization':'Cybersecurity','success_rate':87,'phone':'+971-4-555-0104','email':'layla.h@dubaiworkforce.com','experience':8,'placed':950},
        {'name':'Karim El-Sayed','specialization':'Data Science & AI','success_rate':89,'phone':'+971-4-555-0105','email':'karim.e@dubaiworkforce.com','experience':6,'placed':700},
    ],
    'tokyo': [
        {'name':'Yuki Tanaka','specialization':'Game Dev & C++ Engineering','success_rate':91,'phone':'+81-3-5555-0101','email':'y.tanaka@tokyoworkforce.com','experience':12,'placed':1800},
        {'name':'Hiroshi Yamamoto','specialization':'Embedded & Automotive','success_rate':89,'phone':'+81-3-5555-0102','email':'h.yamamoto@tokyoworkforce.com','experience':15,'placed':2200},
        {'name':'Akiko Sato','specialization':'AI & Data Science','success_rate':90,'phone':'+81-3-5555-0103','email':'a.sato@tokyoworkforce.com','experience':8,'placed':1100},
        {'name':'Kenji Watanabe','specialization':'Web & Full Stack','success_rate':87,'phone':'+81-3-5555-0104','email':'k.watanabe@tokyoworkforce.com','experience':9,'placed':1400},
        {'name':'Yuko Ito','specialization':'Mobile & iOS/Android','success_rate':86,'phone':'+81-3-5555-0105','email':'y.ito@tokyoworkforce.com','experience':7,'placed':900},
    ],
    'sydney': [
        {'name':'Liam Anderson','specialization':'Full Stack & Cloud','success_rate':90,'phone':'+61-2-9555-0101','email':'l.anderson@sydneyworkforce.com','experience':11,'placed':1700},
        {'name':'Charlotte Williams','specialization':'Data & AI','success_rate':92,'phone':'+61-2-9555-0102','email':'c.williams@sydneyworkforce.com','experience':8,'placed':1100},
        {'name':'Noah Johnson','specialization':'Cybersecurity','success_rate':88,'phone':'+61-2-9555-0103','email':'n.johnson@sydneyworkforce.com','experience':9,'placed':1000},
        {'name':'Olivia Jones','specialization':'Mobile & Frontend','success_rate':87,'phone':'+61-2-9555-0104','email':'o.jones@sydneyworkforce.com','experience':7,'placed':850},
        {'name':'Ethan Brown','specialization':'DevOps & SRE','success_rate':89,'phone':'+61-2-9555-0105','email':'e.brown@sydneyworkforce.com','experience':10,'placed':1300},
    ],
    'toronto': [
        {'name':'Emma MacDonald','specialization':'ML/AI & Data Science','success_rate':93,'phone':'+1-416-555-0101','email':'emma.m@torontoworkforce.com','experience':9,'placed':1400},
        {'name':'William Lee','specialization':'Full Stack & Backend','success_rate':89,'phone':'+1-416-555-0102','email':'w.lee@torontoworkforce.com','experience':11,'placed':1700},
        {'name':'Isabella Garcia','specialization':'FinTech & Banking','success_rate':87,'phone':'+1-416-555-0103','email':'i.garcia@torontoworkforce.com','experience':8,'placed':1000},
        {'name':'Lucas Martin','specialization':'Cloud & DevOps','success_rate':91,'phone':'+1-416-555-0104','email':'l.martin@torontoworkforce.com','experience':10,'placed':1500},
        {'name':'Sophia Wilson','specialization':'Cybersecurity','success_rate':88,'phone':'+1-416-555-0105','email':'s.wilson@torontoworkforce.com','experience':7,'placed':850},
    ],
    'vizag': [
        {'name':'Venkata Rao','specialization':'Software & IT Recruitment','success_rate':88,'phone':'+91-891-2345-101','email':'venkata.r@vizagworkforce.com','experience':13,'placed':1800},
        {'name':'Lakshmi Devi','specialization':'IT & Data Science','success_rate':86,'phone':'+91-891-2345-102','email':'lakshmi.d@vizagworkforce.com','experience':8,'placed':900},
        {'name':'Suresh Babu','specialization':'DevOps & Cloud','success_rate':84,'phone':'+91-891-2345-103','email':'suresh.b@vizagworkforce.com','experience':7,'placed':700},
        {'name':'Anitha Kumari','specialization':'Full Stack & Frontend','success_rate':87,'phone':'+91-891-2345-104','email':'anitha.k@vizagworkforce.com','experience':9,'placed':1100},
        {'name':'Ravi Teja','specialization':'Embedded & IoT','success_rate':85,'phone':'+91-891-2345-105','email':'ravi.t@vizagworkforce.com','experience':6,'placed':500},
    ],
}

def extract_skills_from_text(text):
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return list(set(found))

def extract_years_experience(text):
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'experience\s*(?:of\s*)?(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience',
    ]
    for pat in patterns:
        m = re.search(pat, text.lower())
        if m:
            return int(m.group(1))
    return 0

def score_job(job, resume_skills, resume_years):
    job_skills_lower = [s.lower() for s in job['skills']]
    resume_lower = [s.lower() for s in resume_skills]
    if job_skills_lower:
        matched = sum(1 for s in job_skills_lower if s in resume_lower)
        skill_score = int((matched / len(job_skills_lower)) * 100)
    else:
        skill_score = 0
    req_text = job.get('experience', '0-2 yrs')
    exp_nums = re.findall(r'\d+', req_text)
    if exp_nums:
        req_min = int(exp_nums[0])
        req_max = int(exp_nums[-1]) if len(exp_nums) > 1 else req_min + 2
        if resume_years == 0:
            exp_score = 50
        elif resume_years >= req_min:
            over = resume_years - req_max
            exp_score = 100 if over <= 0 else max(60, 100 - over * 5)
        else:
            diff = req_min - resume_years
            exp_score = max(0, 80 - diff * 20)
    else:
        exp_score = 50
    overall = int(skill_score * 0.6 + exp_score * 0.4)
    return {'skill_match': skill_score, 'experience_match': exp_score, 'overall_score': overall}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cities')
def get_cities():
    return jsonify({'cities': sorted(JOBS_DATA.keys())})

@app.route('/api/jobs/<city>')
def get_jobs(city):
    city = city.lower()
    jobs = JOBS_DATA.get(city)
    if jobs is None:
        return jsonify({'error': f'City not found'}), 404
    category = request.args.get('category', 'all')
    if category != 'all':
        jobs = [j for j in jobs if category in j.get('category', [])]
    return jsonify({'city': city, 'jobs': jobs, 'total': len(jobs)})

@app.route('/api/companies/<city>')
def get_companies(city):
    city = city.lower()
    companies = COMPANIES_DATA.get(city)
    if companies is None:
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'city': city, 'companies': companies, 'total': len(companies)})

@app.route('/api/startups/<city>')
def get_startups(city):
    city = city.lower()
    startups = STARTUPS_DATA.get(city)
    if startups is None:
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'city': city, 'startups': startups, 'total': len(startups)})

@app.route('/api/officers/<city>')
def get_officers(city):
    city = city.lower()
    officers = OFFICERS_DATA.get(city)
    if officers is None:
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'city': city, 'officers': officers, 'total': len(officers)})

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['resume']
    city = request.form.get('city', '').strip().lower()
    if not city:
        return jsonify({'error': 'Please select a city'}), 400
    jobs = JOBS_DATA.get(city)
    if jobs is None:
        return jsonify({'error': 'City not found'}), 404
    filename = (file.filename or '').lower()
    text = ''
    try:
        file_bytes = file.read()
        if filename.endswith('.pdf'):
            import pdfplumber
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + '\n'
        elif filename.endswith('.docx'):
            from docx import Document
            doc = Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + '\n'
        else:
            text = file_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        return jsonify({'error': f'Failed to parse resume: {str(e)}'}), 400
    if not text.strip():
        return jsonify({'error': 'Could not extract text from resume'}), 400
    resume_skills = extract_skills_from_text(text)
    resume_years = extract_years_experience(text)
    scored = []
    for job in jobs:
        scores = score_job(job, resume_skills, resume_years)
        scored.append({**job, **scores})
    scored.sort(key=lambda x: x['overall_score'], reverse=True)
    return jsonify({
        'city': city,
        'extracted_skills': resume_skills,
        'experience_years': resume_years,
        'recommendations': scored[:10],
        'total_jobs_analyzed': len(jobs),
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json.get('data', '').strip().lower()
        if not data:
            return jsonify({'result': 'Please enter a city name'}), 400
        jobs = JOBS_DATA.get(data)
        if jobs is None:
            return jsonify({'result': f'City not found. Available: {", ".join(sorted(JOBS_DATA.keys()))}'}), 404
        result = f"Workforce Gap Analysis for {data.title()}\n" + "="*50 + "\n"
        for j in jobs:
            result += f"\u2022 {j['role']} \u2014 {j['openings']} openings \u2014 {j['salary']}\n"
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'result': f'Error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
