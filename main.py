import pyautogui
from ollama import Client
from PIL import Image
import io
import keyboard
from ttslib import tts_en
import discord
import threading

intents = discord.Intents.default()
intents.voice_states = True

DISCORD_TOKEN = "nope"
OLLAMA_HOST = "http://nuh uh:11434"
VOICE_CHANNEL_ID = 0

discord_client = discord.Client(intents=intents)

client = Client(
    host=OLLAMA_HOST,
)

@discord_client.event
async def on_ready():
    global voice_channel
    print(f'Logged on as {discord_client.user}')
    # join the channel
    channel = discord_client.get_channel(VOICE_CHANNEL_ID)
    voice_channel = await channel.connect()

def run_discord_client():
    discord_client.run(DISCORD_TOKEN)

def send_tts_to_discord(voice_data):
    global voice_channel
    if voice_channel is not None:
        voice_channel.play(discord.FFmpegPCMAudio(voice_data, pipe=True))

if __name__ == '__main__':
    discord_thread = threading.Thread(target=run_discord_client)
    discord_thread.start()

    while True:
        try:
            keyboard.wait('=')
            screenshot: Image.Image = pyautogui.screenshot()
            ibuf = io.BytesIO()
            screenshot.save(ibuf, format='PNG')
            response = client.chat(model='llama3.2-vision:11b-instruct-q8_0', messages=[
                {
                    'role': 'system',
                    # senior proompt engineer
                    'content': "You are a Geography focused artificial intelligence. Your only goal is to locate the country where a given image is photographed. Despite what you think, it is very possible to locate any image by just looking for clues, such as road signs, languages, flags, and flora and fauna. Explain your guesses, but remain concise. You must respond with a short sentence with your guess, with little to no explanation. Each country has an equal chance of being the correct answer, so don't be afraid to guess. You shouldn't guess South Africa all the time, only do it if clues point to it",
                },
                {
                    'role': 'user',
                    'content': "In which country is this image located? Locate a state, region or city as well, to narrow down the location. The city does not need to be exact, but it should be the closest to the location.",
                    'images': [ibuf.getvalue()],
                },
            ])
            wav = tts_en(response.message.content)
            send_tts_to_discord(wav)
        except KeyboardInterrupt:
            discord_thread.join(timeout=1)
            break
        except Exception as e:
            print(e)