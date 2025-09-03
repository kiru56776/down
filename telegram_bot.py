# telegram_bot.py
# This is the main file for our YouTube Downloader Telegram Bot.
# It uses the python-telegram-bot library to handle Telegram's API,
# and yt-dlp to search for and download videos from YouTube.

import logging
import os
import re
from uuid import uuid4

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from yt_dlp import YoutubeDL

# --- Configuration ---
# It's highly recommended to use environment variables for sensitive data like bot tokens.
# When you deploy to Render, you'll set these in the environment settings.
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN_HERE')
DOWNLOAD_DIR = 'downloads'

# --- Logging Setup ---
# This helps in debugging by printing informative messages to the console.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- State Management ---
# This dictionary will act as a simple in-memory "database" to store
# search results for each user (chat_id).
user_search_results = {}

# --- Helper Functions ---

def clean_filename(filename):
    """
    Removes invalid characters from a filename to make it safe for saving.
    """
    return re.sub(r'[\\/:*?"<>|]', '-', filename)

async def search_youtube(query: str, max_results: int = 5) -> list:
    """
    Searches YouTube using yt-dlp and returns a list of video results.
    Each result is a dictionary containing title and video_id.
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'default_search': f"ytsearch{max_results}",
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(query, download=False)
            if 'entries' in search_result:
                videos = []
                for entry in search_result['entries']:
                    videos.append({
                        'id': entry['id'],
                        'title': entry['title'],
                        'url': f"https://www.youtube.com/watch?v={entry['id']}"
                    })
                return videos
    except Exception as e:
        logger.error(f"Error searching YouTube: {e}")
        return []
    return []


# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for the /start command.
    Greets the user and provides instructions.
    """
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Hello, {user_name}!\n\n"
        "I'm your YouTube Downloader Bot.\n\n"
        "Here's how to use me:\n"
        "1. **Send a YouTube Link**: I'll download the video for you directly.\n\n"
        "2. **Search for Videos**: Type `Search <number> <video name>`.\n"
        "   - Example: `Search 5 latest ethiopian news`\n\n"
        "3. **Download from Search**: After searching, type `Download <number>` to get a specific video.\n"
        "   - Example: `Download 3` to download the 3rd video from the search results.\n"
        "   - You can also type `Download all` to get all videos from the results one by one."
    )

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles search queries like "Search 5 latest news".
    """
    chat_id = update.message.chat_id
    text = update.message.text

    match = re.match(r'Search\s+(\d+)\s+(.+)', text, re.IGNORECASE)

    if not match:
        await update.message.reply_text("❌ Invalid search format. Please use: `Search <number> <video name>`")
        return

    num_videos = int(match.group(1))
    query = match.group(2)

    if not 1 <= num_videos <= 10:
        await update.message.reply_text("Please request between 1 and 10 videos.")
        return

    await update.message.reply_text(f"Searching for the top {num_videos} videos about '{query}'...")
    videos = await search_youtube(query, max_results=num_videos)

    if not videos:
        await update.message.reply_text("Sorry, I couldn't find any videos for your search.")
        return

    user_search_results[chat_id] = videos
    response_message = "Here are the results:\n\n"
    for i, video in enumerate(videos, 1):
        response_message += f"{i}. {video['title']}\n"
    response_message += "\nTo download, reply with `Download <number>` (e.g., `Download 1`)."
    await update.message.reply_text(response_message)

async def handle_download_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles download commands like "Download 3" or "Download all".
    """
    chat_id = update.message.chat_id
    text = update.message.text.lower()

    if chat_id not in user_search_results:
        await update.message.reply_text("You need to search for videos first! Use the `Search` command.")
        return

    videos_to_download = []
    if text == 'download all':
        videos_to_download = user_search_results[chat_id]
    else:
        match = re.match(r'download\s+(\d+)', text)
        if match:
            video_index = int(match.group(1)) - 1
            if 0 <= video_index < len(user_search_results[chat_id]):
                videos_to_download.append(user_search_results[chat_id][video_index])
            else:
                await update.message.reply_text("Invalid video number. Please choose a number from the list.")
                return
        else:
            await update.message.reply_text("Invalid download command. Use `Download <number>` or `Download all`.")
            return

    if not videos_to_download:
        await update.message.reply_text("Couldn't find the video(s) to download.")
        return

    for video in videos_to_download:
        await download_and_send_video(update, context, video['url'])


async def download_and_send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str) -> None:
    """
    Downloads a video from a given URL and sends it to the user.
    """
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    status_message = await update.message.reply_text("Starting download... ⏳")

    # --- START OF DEBUGGING CODE ---
    current_directory = os.getcwd()
    logger.info(f"Current working directory: {current_directory}")
    files_in_directory = os.listdir(current_directory)
    logger.info(f"Files in directory: {files_in_directory}")
    # --- END OF DEBUGGING CODE ---

    cookie_file_path = 'cookies.txt'
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: progress_hook(d, status_message, context.bot)],
        'noplaylist': True,
    }

    if os.path.exists(cookie_file_path):
        logger.info(f"SUCCESS: Found '{cookie_file_path}' and will use it for download.")
        ydl_opts['cookiefile'] = cookie_file_path
    else:
        logger.warning(f"WARNING: '{cookie_file_path}' not found. Proceeding without authentication. This may fail.")

    filepath = None
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            if os.path.exists(downloaded_file):
                filepath = downloaded_file
            else:
                logger.error(f"File not found at expected path: {downloaded_file}")
                await status_message.edit_text("❌ Error: Downloaded file not found on server.")
                return
    except Exception as e:
        logger.error(f"Error during video download: {e}")
        error_message = str(e)
        if "confirm you’re not a bot" in error_message:
            await status_message.edit_text("❌ Download failed: YouTube is blocking the request. The cookie file might be expired or invalid.")
        else:
            await status_message.edit_text(f"❌ An error occurred during download.")
        return

    if filepath and os.path.exists(filepath):
        await status_message.edit_text("Download complete! Now uploading to Telegram... 🚀")
        try:
            if os.path.getsize(filepath) > 50 * 1024 * 1024:
                await update.message.reply_text(
                    f"⚠️ The video '{os.path.basename(filepath)}' is larger than 50MB and cannot be sent via Telegram."
                )
            else:
                with open(filepath, 'rb') as video_file:
                    await update.message.reply_video(video=video_file, caption=os.path.basename(filepath))
        except Exception as e:
            logger.error(f"Error uploading video to Telegram: {e}")
            await update.message.reply_text("❌ Failed to upload the video to Telegram.")
        finally:
            os.remove(filepath)
            await status_message.delete()
    else:
        await status_message.edit_text("❌ Could not find the downloaded file to send.")


def progress_hook(d, status_message, bot):
    """
    A hook function for yt-dlp to report download progress.
    """
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        logger.info(f"Downloading: {percent} at {speed}, ETA {eta}")
    elif d['status'] == 'finished':
        logger.info("Download finished, preparing to upload...")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    The main message handler. It checks the message text to decide what to do.
    """
    text = update.message.text
    if not text:
        return

    if 'youtube.com/' in text or 'youtu.be/' in text:
        await download_and_send_video(update, context, text)
    elif text.lower().startswith('search '):
        await handle_search(update, context)
    elif text.lower().startswith('download '):
        await handle_download_command(update, context)
    else:
        await update.message.reply_text(
            "I'm not sure what you mean. Please send a YouTube link, or use the `Search` or `Download` commands."
        )


def main() -> None:
    """
    The main function to start the bot.
    """
    if TELEGRAM_TOKEN == 'YOUR_TELEGRAM_BOT_TOKEN_HERE':
        logger.error("Telegram bot token not set! Please set the TELEGRAM_TOKEN environment variable.")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()

