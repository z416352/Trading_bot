from datetime import datetime


class MessageErrorException(Exception):
    def __init__(self, message, url):
        message = f'{message}\n Url: {url} \n'
        super().__init__(message)
        
class MessageEmptyException(Exception):
    def __init__(self, message, start, end):
        start = str(datetime.fromtimestamp(int(float(start)) / 1000))
        end = str(datetime.fromtimestamp(int(float(end)) / 1000))

        message = f'{message}\n start time: {start}\n end time: {end}\n'
        super().__init__(message)