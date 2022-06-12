
import re

YOU_TUBE_URL_REGEX = '(?:https?:\/\/)?(?:(?:(?:www\.?)?youtube\.com(?:\/(?:(?:watch\?.*?(v=[^&\s]+).*)|(?:v(\/.*))|(channel\/.+)|(?:user\/(.+))|(?:results\?(search_query=.+))))?)|(?:youtu\.be(\/.*)?))'

def is_youtube_url(url:str):
    matches = re.search(YOU_TUBE_URL_REGEX,url)
    return matches is not None