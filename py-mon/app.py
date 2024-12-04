import requests
import time
from requests.auth import HTTPBasicAuth
import json

GITLAB_API_URL = "https://gitlab.com/api/v4/projects/ElnurBDa%2Fethical-hacking-proj/trigger/pipeline"
PRIVATE_TOKEN = "glpat***"
TRIGGER_TOKEN = "glptt***"
REF = "main"  

def trigger_pipeline():
    url = GITLAB_API_URL
    headers = {
        "PRIVATE-TOKEN": PRIVATE_TOKEN
    }
    data = {
        "token": TRIGGER_TOKEN,
        "ref": REF
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 201:
        print("Pipeline triggered successfully!")
        print("Response:", response.json())
    else:
        print("Failed to trigger pipeline.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

url = ""

username = 'elastic'
password = ''

query_payload = {
    "query": {
        "range": {
            "@timestamp": {
                "gte": "now-3m/m",
                "lte": "now",
                "format": "strict_date_optional_time"
            }
        }
    }
}

headers = {
    'Content-Type': 'application/json',
    'Host': 'yelka.us-central1-b.c.getmoney-437018.internal'
}

def check_alerts():
    try:
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password), json=query_payload, verify=False)
        
        if response.status_code == 200:
            result = response.json()

            if result['hits']['total']['value'] > 0:
                print("Alert(s) found:")
                for hit in result['hits']['hits']:
                    print(json.dumps(hit, indent=2))
                trigger_pipeline()
            else:
                print("No alerts found in the last 1 minute.")
        else:
            print(f"Error: Received status code {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    check_alerts()
    time.sleep(60)
