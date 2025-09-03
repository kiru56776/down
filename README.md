🚀 YouTube Downloader Telegram Bot 🚀

Welcome to your personal YouTube Downloader Telegram Bot! This powerful yet simple bot allows you to grab videos directly from YouTube without ever leaving your Telegram chat.

✨ Core Features

🔗 Direct Download: Simply send any YouTube video link to the bot, and it will download and send the video back to you.

🔍 Powerful Video Search: Can't remember the link? No problem! Use the search command to find videos.

Example: Search 5 latest Ethiopian news

🔢 Selective Download: After searching, you can download a specific video by its number from the list.

Example: Download 3

📥 Download All: Want all the videos from your search? Just type Download all, and the bot will fetch them for you one by one.

🛠️ How to Set Up and Deploy on Render

Follow these steps to launch your very own instance of this bot. We'll use GitHub for storing the code and Render for hosting it online 24/7.

Step 1: Create Your Telegram Bot

First, you need to get your bot's "key," which is an API token from Telegram itself.

Talk to the BotFather: Open your Telegram app and search for the official @BotFather account (it has a blue checkmark).

Create a New Bot: Start a chat with BotFather and send the /newbot command.

Choose a Name & Username:

First, give your bot a friendly display name (e.g., KT's Video Bot).

Next, choose a unique username that must end in bot (e.g., KTsVideoDownloader_bot).

🔑 Get Your API Token: BotFather will congratulate you and provide a long HTTP API token. It will look something like 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11.

This token is your bot's password. Copy it immediately and keep it safe!

Step 2: Set Up Your GitHub Repository

This is where your bot's code will live.

Create a GitHub Account: If you don't have one, sign up for free at GitHub.com.

Create a New Repository: Click the + icon in the top right and select "New repository". You can make it public or private.

Upload the Project Files: In your new repository, upload the three files I provided:

telegram_bot.py

requirements.txt

README.md (this file!)

Step 3: Deploy the Bot on Render

Render is a cloud service that will run your bot for free.

Sign Up for Render: Create a free account at Render.com.

Create a New "Web Service":

From your Render dashboard, click "New +" and choose "Web Service".

Connect your GitHub account and select the repository you just created.

Configure the Service Settings:

Name: Give your service a unique name (e.g., kt-telegram-bot).

Region: Choose a region that is geographically close to you.

Branch: Select your main branch (usually main or master).

Runtime: Render should automatically detect Python 3.

Build Command: This should default to pip install -r requirements.txt. This is correct.

Start Command: Enter the command python telegram_bot.py.

Instance Type: The Free tier is perfect for this bot.

Add Your Secret Token (CRUCIAL STEP!):

Before you deploy, scroll down and find the "Environment" section.

Click "Add Environment Variable".

For the Key, enter exactly: TELEGRAM_TOKEN

For the Value, paste the HTTP API token you saved from BotFather.

Click "Save Changes". This keeps your token secure and out of your code.

🚀 Launch!:

Scroll to the bottom and click the "Create Web Service" button.

Render will now build and start your bot. You can monitor the progress in the "Logs" tab. Once you see a message like Bot is starting..., your bot is live!

Step 4: Start Chatting With Your Bot!

Open Telegram, search for your bot by its username, and send the /start command. It's now ready to follow your commands!

⚠️ Important Note: Telegram has a file size limit of 50MB for bots. This bot will automatically check the file size and warn you if a video is too large to be uploaded.
