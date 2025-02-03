# llama-geoguessr
forcing llama 3.2 to play geoguessr

## how does it work?
- when the = key is pressed on the keyboard, a screenshot is taken
- the screenshot is sent sent to Ollama, running locally or on a remote server.
- the llama-3.2-vision model picks it up and tries to guess where the image was taken.
- the AI's answer is then read aloud through the MeloTTS library, over a Discord bot
- a human finds the location and guesses there

## how to run it?
- clone the repo
- create a new venv in the repo folder
- install [MeloTTS](https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md)
- pip install `pyautogui ollama Pillow keyboard discord.py numpy scipy`
- fill out the constants in main.py (you will need an Ollama installation with the `llama3.2-vision:11b-instruct-q8_0` model available, a Discord bot, and a voice channel ID for the bot to join)
- try it! both starting the bot and the first generation will be slower than the rest. I get speeds up to ~5 sec per end-to-end generation. 
