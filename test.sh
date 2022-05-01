curl --location --request POST 'https://api.notion.com/v1/databases/' \
--header 'Authorization: Bearer secret_UYq6njw7326NBg52vqklmxmVpZkj1QXRt5cvAKLqaaW' \
--header 'Content-Type: application/json' \
--header 'Notion-Version: 2022-02-22' \
--data '{
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
                "link": null
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
}'
