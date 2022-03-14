from aiogram import types
from pytube import Stream,StreamQuery
from callback_type import CallbackType
import callback_data
import size_converter

def build_preview_markup(streams:StreamQuery):
    markup = types.InlineKeyboardMarkup()
    for stream in streams:
        button_text = f'{stream.resolution} ({size_converter.get_human_readable_text(stream.filesize)})'
        item = types.InlineKeyboardButton(button_text,callback_data=_get_payload(stream))
        markup.add(item)
    return markup

def _get_payload(stream:Stream):
    print(stream.url)
    itag = stream.itag
    return callback_data.preview_callback.new(
        evt=CallbackType.INLINE_KEYBOARD, 
        itag=itag
    )