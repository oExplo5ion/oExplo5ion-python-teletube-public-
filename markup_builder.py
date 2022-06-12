import imp
from re import U
from aiogram import types
from pytube import Stream,StreamQuery
from callback_type import CallbackType
import callback_data
import size_converter

def build_preview_markup(url:str, streams:StreamQuery):
    markup = types.InlineKeyboardMarkup()
    for stream in streams:
        button_text = f'{stream.resolution} ({size_converter.get_human_readable_text(stream.filesize)})'
        item = types.InlineKeyboardButton(button_text,callback_data=_get_payload(url,stream))
        markup.add(item)
    return markup

def _get_payload(url:str, stream:Stream):
    itag = stream.itag
    url_correct = url.replace('https://youtube.com/watch?v=','')
    return callback_data.preview_callback.new(
        evt=CallbackType.INLINE_KEYBOARD, 
        itag=itag,
        url=url_correct
    )