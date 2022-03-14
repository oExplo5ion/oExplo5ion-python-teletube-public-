from unittest import installHandler
from pytube import YouTube,Stream,StreamQuery
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
import firebase_helper

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot)
streams:StreamQuery = None

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
    # get video url
    await message.reply(strings.FETCHING_DATA,reply=False)
    tube = e_you_tube.get_tube(message.text)
    if tube is None:
        await message.answer(strings.ERROR)
        return
    # reply with error
    if isinstance(tube,EUError):
        await message.reply(tube.error)
    # show user preview with resoultions buttons
    await show_preview_options(message,tube)

@dispatcher.callback_query_handler(callback_data.preview_callback.filter())
async def callback(call:types.CallbackQuery, callback_data: dict):
    """
        React to buttons callback
    """
    global streams
    message = call.message
    if streams is None:
        await message.reply(strings.COULD_BOT_GET_VIDEO,reply=False)
        return
    if len(streams) <= 0:
        await message.reply(strings.COULD_BOT_GET_VIDEO,reply=False)
        return
    itag = callback_data.get('itag')
    stream = streams.get_by_itag(itag)
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
    markup = markup_builder.build_preview_markup(streams=streams)
    await message.reply_photo(
        photo=tube.thumbnail_url,
        reply=False,
        caption=strings.CHOOSE_RESOLUTION,
        reply_markup=markup
    )

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher, skip_updates=True)