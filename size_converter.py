
def get_human_readable_text(size:int):
    if size < 1024:
        return f'{size} B'
    elif size < 1024*1024:
        return f'{round(size/1024, 2)} KB'
    elif size < 1024*1024*1024:
        return f'{round(size/(1024*1024), 2)} MB'
    elif size < 1024*1024*1024*1024:
        return f'{round(size/(1024*1024*1024), 2)} GB'