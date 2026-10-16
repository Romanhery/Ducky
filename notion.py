import os
from notion_client import Client
from dotenv import load_dotenv
load_dotenv()
notion = Client(auth=os.environ["NOTION_API_KEY"]) 

users = notion.users.list()

for user in users.get("results"):
    name, user_type = user["name"], user["type"]
    emoji = "😅" if user["type"] == "bot" else "🙋‍♂️"
    print(f"{name} is a {user_type} {emoji}")
