from pytube import YouTube
from e_u_error import EUError
import strings

def get_tube(url:str):
    """
        Get streams of provided YouTube url
    """
    try:
        yt = YouTube(url)
        # raises error if streams not avalable
        yt.streams
        return yt
    except Exception as e:
        return EUError(strings.COULD_BOT_GET_VIDEO)

def get_preview_streams(tube:YouTube):
    """
        Returns streams of provided YouTube object
    """
    try:
        streams = tube.streams
        if len(streams) <= 0:
            return EUError(strings.COULD_BOT_GET_VIDEO)
        return streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    except Exception as e:
        return EUError(strings.COULD_BOT_GET_VIDEO)

