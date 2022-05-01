import requests
import json

def send_to_notion(assignments, database_id, api_key):
    for assignment in assignments:
        url = 'https://api.notion.com/v1/pages'

        payload = json.dumps({
            'parent': {
                'database_id': database_id
            },
            'properties': {
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': assignment['name']
                            }
                        }
                    ]
                },
                'date': {
                    'type': 'date',
                    'date': {
                        'start': assignment['start date and time'],
                        'end': assignment['end date and time']
                    }
                },
                'course': {
                    'select': {
                        'name': assignment['course']
                    }
                },
                'source_name': {
                    'select': {
                        'name': assignment['source_name']
                    }
                },
                'type': {
                    'select': {
                        'name': assignment['type']
                    }
                }
            }
        })

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-08-16'
        }

        response = requests.request('POST', url, headers=headers, data=payload)

        print(response.text)

def setup_table(database_id, api_key):
    url = f'https://api.notion.com/v1/databases/{database_id}'

    payload = json.dumps({
        "properties": {
            "type": {
                "select": {
                    "options": []
                }
            },
            "course": {
                "select": {
                    "options": []
                }
            },
            "date": {
                "date": {}
            },
            "source_name": {
                "select": {
                    "options": []
                }
            }
        }
    })

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-02-22'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    print(response.text)
