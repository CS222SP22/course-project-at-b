# curl --location --request POST 'https://api.notion.com/v1/databases/' \
# --header 'Authorization: Bearer secret_UYq6njw7326NBg52vqklmxmVpZkj1QXRt5cvAKLqaaW' \
# --header 'Content-Type: application/json' \
# --header 'Notion-Version: 2022-02-22' \
# --data-raw '{
#     "parent": {
#         "type": "page_id",
#         "page_id": "f99bff67095d4241b518dedb1a01d648"
#     },
#     "icon": {
#     	"type": "emoji",
#         "emoji": "📚"
#   	},
#   	"cover": {
#   		"type": "external",
#     	"external": {
#     		"url": "https://cdn.cdnparenting.com/articles/2018/06/471582446_H.webp"
#     	}
#   	},
#     "title": [
#         {
#             "type": "text",
#             "text": {
#                 "content": "Assigment Aggregator",
#                 "link": null
#             }
#         }
#     ],
#     "properties": {
#         "name": {
#             "title": {}
#         },
#         "type": {
#            "select": {
#                 "options": []
#             } 
#         },
#         "course": {
#            "select": {
#                 "options": []
#             } 
#         },
#         "start date": {
#             "date": {}
#         },
#         "end date": {
#             "date": {}
#         },
#         "start date and time": {
#             "date": {}
#         },
#         "end date and time": {
#             "date": {}
#         },
#         "source_name": {
#            "select": {
#                 "options": []
#             } 
#         }
#     }
# }'

# curl --location --request POST 'https://api.notion.com/v1/pages' \
# --header 'Authorization: Bearer secret_UYq6njw7326NBg52vqklmxmVpZkj1QXRt5cvAKLqaaW' \
# --header 'Content-Type: application/json' \
# --header 'Notion-Version: 2021-08-16' \
# --data-raw '{
#   "parent": {
#     "database_id": "6a7eb96f-88a4-4cad-9dd0-821e691834ab"
#   },
#   "properties": {
#     "name": {
#       "title": [{"text": {"content": "my assignment title"}}]
#     },
#     "course": {
#       "select": {
#         "name": "CS 233"
#       }
#     },
#     "source_name": {
#       "select": {
#         "name": "CBTF"
#       }
#     }
#   }
# }'

import requests
import json

url = "https://api.notion.com/v1/pages"

payload = json.dumps({
  "parent": {
    "database_id": "6a7eb96f-88a4-4cad-9dd0-821e691834ab"
  },
  "properties": {
    "name": {
      "title": [
        {
          "text": {
            "content": "my assignment title"
          }
        }
      ]
    },
    "course": {
      "select": {
        "name": "CS 233"
      }
    },
    "source_name": {
      "select": {
        "name": "CBTF"
      }
    }
  }
})
headers = {
  'Authorization': 'Bearer secret_UYq6njw7326NBg52vqklmxmVpZkj1QXRt5cvAKLqaaW',
  'Content-Type': 'application/json',
  'Notion-Version': '2021-08-16'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

url = "https://api.notion.com/v1/databases/"

payload = json.dumps({
  "parent": {
    "type": "page_id",
    "page_id": "f99bff67095d4241b518dedb1a01d648"
  },
  "icon": {
    "type": "emoji",
    "emoji": "📚"
  },
  "cover": {
    "type": "external",
    "external": {
      "url": "https://cdn.cdnparenting.com/articles/2018/06/471582446_H.webp"
    }
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "Assigment Aggregator",
        "link": None
      }
    }
  ],
  "properties": {
    "name": {
      "title": {}
    },
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
    "start date": {
      "date": {}
    },
    "end date": {
      "date": {}
    },
    "start date and time": {
      "date": {}
    },
    "end date and time": {
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
  'Authorization': 'Bearer secret_UYq6njw7326NBg52vqklmxmVpZkj1QXRt5cvAKLqaaW',
  'Content-Type': 'application/json',
  'Notion-Version': '2022-02-22'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

