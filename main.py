from pytube import YouTube,Stream
from e_u_error import EUError
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import InvalidHTTPUrlContent
from config import TOKEN
import callback_data
import logging
import markup_builder
import regex
import commands
import e_you_tube
import strings

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot)

# EXAMPLE = 'https://www.youtube.com/watch?v=hS5CfP8n_js'

# decorators
@dispatcher.message_handler()
async def echo(message: types.Message):
    """
        Detects context of message and tries to react to it
    """
    #  check commands
    if message.text == commands.COMMAND_START:
        await message.answer(strings.SEND_ME_A_YOUTUBE_LINK)
        return
    # check is YouTube url
    if regex.is_youtube_url(message.text) is False:
        await message.answer(strings.DOES_NOT_LOOK_LIKE_A_YOUTUBE_LINK)
        return
    if len(message.text) >= 60:
        await message.answer(strings.LONG_LINKS_NOT_SUPPORTED)
        return
    # get video url
    await message.reply(strings.FETCHING_DATA,reply=False)
    tube = e_you_tube.get_tube(message.text)
    if tube is None:
        await message.answer(strings.ERROR)
        return
    # reply with error
    if isinstance(tube,EUError):
        await message.reply(tube.error)
        return
    # show user preview with resoultions buttons
    await show_preview_options(message,tube)

@dispatcher.callback_query_handler(callback_data.preview_callback.filter())
async def callback(call:types.CallbackQuery, callback_data: dict):
    """
        React to buttons callback
    """
    message = call.message
    itag = callback_data.get('itag')
    url = callback_data.get('url')
    if url is None:
        await message.reply(strings.COULD_BOT_GET_VIDEO,reply=False)
        return

    tube = e_you_tube.get_tube(f'https://youtube.com/watch?v={url}')
    if tube is None:
        await message.answer(strings.ERROR)
        return
    if isinstance(tube,EUError):
        await message.reply(tube.error)
        return
    stream = tube.streams.get_by_itag(itag)
    if stream is None:
        await message.answer(strings.ERROR)
        return
    await send_video_from_stream(message,stream)
    

# business logic
async def send_video_from_stream(message:types.Message,stream:Stream):
    """
        Replry user with video from the stream
    """
    # download video and send to user
    media = [types.InputMediaVideo(media=stream.url)]
    try:
        await message.reply_media_group(media=media, reply=False)
    except InvalidHTTPUrlContent:
        await message.reply(strings.COULD_BOT_GET_VIDEO,reply=False)

async def show_preview_options(message:types.Message,tube:YouTube):
    """
        Show preview with resolution buttons
    """
    # get streams
    global streams
    streams = e_you_tube.get_preview_streams(tube)
    if isinstance(streams,EUError):
        await message.reply(streams.error)
    # get resolution buttons markup
    markup = markup_builder.build_preview_markup(url=tube.watch_url,streams=streams)
    await message.reply_photo(
        photo=tube.thumbnail_url,
        reply=False,
        caption=strings.CHOOSE_RESOLUTION,
        reply_markup=markup
    )

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher, skip_updates=True)
    # firebase_helper.test()