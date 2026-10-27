import os 
import json
from notion_client import Client
from google import genai
from dotenv import load_dotenv
load_dotenv()
client = genai.Client()

page_id = os.getenv("NOTION_PAGE_ID")
api_key = os.getenv("NOTION_API_KEY")

notion = Client(auth=api_key)

audio_file = client.files.upload(file="/Users/Roman/Desktop/Projects/Ducky/recording.mp3")

interaction = client.interactions.create(
    model="gemini-3.5-transcribe",
    input=[
        {
            "type": "audio",
            "uri": audio_file.uri,
            "mime_type": audio_file.mime_type,
        }
    ],
)
print(interaction.output_text)

def main():
    block_id = page_id  # Blocks can be appended to other blocks *or* pages. Therefore, a page ID can be used for the block_id parameter
    new_heading_response = notion.blocks.children.append(
        block_id=block_id,
        # Pass an array of blocks to append to the page: https://developers.notion.com/reference/block#block-type-objects
        children=[
            {
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Transcription",  # This is the text that will be displayed in Notion
                            },
                        },
                    ],
                },
            },
            {
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": f"{interaction.output_text}",  # This is the text that will be displayed in Notion
                            },
                        },
                    ],
                },
            },            
        ],
    )

    # Print the new block(s) response
    print(json.dumps(new_heading_response, indent=2))


if __name__ == "__main__":
    main()
