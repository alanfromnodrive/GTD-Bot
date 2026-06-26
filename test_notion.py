import requests

NOTION_API_KEY = "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"
NOTION_DATABASE_ID = "e7b3439cbc4b4bad8a1e96c060574f57"

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

url = "https://api.notion.com/v1/pages"
payload = {
    "parent": {"database_id": NOTION_DATABASE_ID},
    "properties": {
        "Name": {"title": [{"text": {"content": "TEST IDEA"}}]},
        "Área": {"select": {"name": "OMG"}},
        "Estado": {"select": {"name": "INBOX"}},
        "Descripción": {"rich_text": [{"text": {"content": "Test desde script"}}]}
    }
}

response = requests.post(url, headers=NOTION_HEADERS, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
