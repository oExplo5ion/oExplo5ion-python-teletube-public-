from distutils.log import error


class EUError:
    error = ''

    def __init__(self,description):
        self.error = description