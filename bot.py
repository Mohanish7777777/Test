from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

def start(update, context):
    update.message.reply_text('Send me a Terabox video URL!')

def handle_message(update, context):
    chat_id = update.message.chat.id
    url = f"https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={update.message.text}"
    
    context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            resolutions = data["response"][0]["resolutions"]
            fast_download_link = resolutions["Fast Download"]
            hd_video_link = resolutions["HD Video"]
            thumbnail_url = data["response"][0]["thumbnail"]
            video_title = data["response"][0]["title"]

            tinyurl_api = "http://tinyurl.com/api-create.php?url="
            tinyurl_fast_download = tinyurl_api + fast_download_link
            tinyurl_hd_video = tinyurl_api + hd_video_link
            shortened_fast_download_link = requests.get(tinyurl_fast_download).text
            shortened_hd_video_link = requests.get(tinyurl_hd_video).text

            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text='➡️ Fast Download', url=shortened_fast_download_link),
                 InlineKeyboardButton(text='▶️ HD Video', url=shortened_hd_video_link)],
                [InlineKeyboardButton(text='Developer', url='t.me/nepcoder')]
            ])

            message_text = f"🎬 <b>Title:</b> {video_title}\nMade with ❤️ by @nepcoder"

            context.bot.send_photo(
                chat_id=chat_id,
                photo=thumbnail_url,
                caption=message_text,
                parse_mode="HTML",
                reply_markup=markup
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="❌ <b>Error fetching data from Terabox API</b>",
                parse_mode="HTML"
            )
    except Exception as e:
        context.bot.send_message(
            chat_id=chat_id,
            text=f"❌ <b>Error: {str(e)}</b>",
            parse_mode="HTML"
        )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
