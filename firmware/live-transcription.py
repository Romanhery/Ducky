import asyncio
import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from notion_client import AsyncClient
import pyaudio

load_dotenv()

# Audio capture configuration (Gemini Live expects 16kHz mono 16-bit PCM)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024  # ~64ms of audio per buffer

# Environment credentials
PAGE_ID = os.getenv("NOTION_PAGE_ID")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Clients
notion = AsyncClient(auth=NOTION_API_KEY)
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-3.5-transcribe-live"

# Transcription configuration
config = types.LiveConnectConfig(
    response_modalities=["TEXT"],
    input_audio_transcription=types.AudioTranscriptionConfig(
        language_codes=[],  # Automatic language detection (85+ languages)
    ),
)


async def send_mic_audio(session, stream):
    """Captures microphone audio frames and streams them to Gemini Live."""
    loop = asyncio.get_running_loop()
    try:
        while True:
            # Delegate blocking audio read to a worker thread
            pcm_bytes = await loop.run_in_executor(
                None, stream.read, CHUNK_SIZE, False
            )

            # Transmit real-time audio chunk wrapped in a Blob
            await session.send_realtime_input(
                audio=types.Blob(
                    data=pcm_bytes,
                    mime_type="audio/pcm;rate=16000",
                )
            )
    except asyncio.CancelledError:
        pass


async def append_to_notion(text: str):
    """Appends finalized transcription as a paragraph block in Notion."""
    try:
        response = await notion.blocks.children.append(
            block_id=PAGE_ID,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": text,
                                },
                            }
                        ],
                    },
                }
            ],
        )
        print(f"\n[Notion Appended]: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"\n[Notion Error] Failed to append block: {e}")


async def receive_transcripts(session):
    """Listens for streaming server events and formats the transcripts."""
    try:
        async for response in session.receive():
            server_content = response.server_content
            if not server_content:
                continue

            # Real-time interim hypothesis (dynamically updates active line)
            if getattr(server_content, "interim_input_transcription", None):
                interim = server_content.interim_input_transcription.text
                print(f"\r[Interim] {interim}", end="", flush=True)

            # Finalized phrase emitted when speech turn or sentence concludes
            if getattr(server_content, "input_transcription", None):
                final_text = server_content.input_transcription.text
                print(f"\n[Final]   {final_text}")

                # Fire off the Notion write without blocking the transcription stream
                asyncio.create_task(append_to_notion(final_text))

    except asyncio.CancelledError:
        pass


async def main():
    p = pyaudio.PyAudio()
    mic_stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    print("Connecting to Gemini Live Transcription...")

    try:
        async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
            print("Connected! Start speaking into your microphone.\n" + "-" * 60)

            # Run microphone capture and transcript reception concurrently
            await asyncio.gather(
                send_mic_audio(session, mic_stream),
                receive_transcripts(session),
            )
    finally:
        mic_stream.stop_stream()
        mic_stream.close()
        p.terminate()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSession stopped.")