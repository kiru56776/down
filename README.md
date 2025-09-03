YouTube Downloader Telegram Bot

This is a simple but powerful Telegram bot that can search for YouTube videos and download them for you directly in your chat.

Features

Direct Download: Send any YouTube video link to the bot to download it.

Video Search: Search for videos using a command like Search 5 latest news.

Selective Download: After a search, download a specific video by its number (e.g., Download 3).

Download All: Download all videos from the search results one by one with Download all.

How to Set Up and Deploy

Follow these steps to get your own instance of this bot running on Render.

Step 1: Create a Telegram Bot

Talk to BotFather: Open Telegram and search for the @BotFather user.

Create a New Bot: Send the /newbot command to BotFather.

Choose a Name and Username: Follow the prompts to give your bot a friendly name (e.g., "My Video Bot") and a unique username (which must end in bot, e.g., MyVideoDownloader_bot).

Get Your Token: BotFather will give you a unique HTTP API token. It will look something like 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11. Copy this token and keep it safe! This is your bot's password.

Step 2: Set Up Your Project on GitHub

Create a GitHub Account: If you don't have one, sign up at GitHub.

Create a New Repository: Create a new public or private repository for this project.

Upload the Files: Upload the three files from this project (telegram_bot.py, requirements.txt, and README.md) into your new repository.

Step 3: Deploy to Render

Sign Up for Render: Create an account on Render.com. They have a free tier that is perfect for this kind of bot.

Create a New Web Service:

On your Render dashboard, click "New +" and select "Web Service".

Connect your GitHub account and select the repository you just created.

Configure the Service:

Name: Give your service a unique name (e.g., my-telegram-bot).

Region: Choose a region close to you.

Branch: Select main or master.

Root Directory: Leave this blank.

Runtime: Render should automatically detect it as a Python project.

Build Command: This should be automatically set to pip install -r requirements.txt.

Start Command: Enter python telegram_bot.py.

Instance Type: The Free tier is sufficient.

Add Environment Variables (Crucial!):

Before deploying, go to the "Environment" tab for your new service.

Click "Add Environment Variable".

For the Key, enter TELEGRAM_TOKEN.

For the Value, paste the HTTP API token you got from BotFather.

Click "Save Changes".

Deploy!:

Click the "Create Web Service" button.

Render will now pull your code from GitHub, install the libraries from requirements.txt, and run your telegram_bot.py script using the start command.

You can watch the deployment progress in the "Logs" tab. If everything is correct, you'll see a message like "Bot is starting...".

Step 4: Use Your Bot!

Open Telegram, find the bot you created, and send the /start command. It should now be fully operational!

Note: Telegram has a 50MB file size limit for bots. This bot will warn you if a video is larger than that size and will not be able to send it.
