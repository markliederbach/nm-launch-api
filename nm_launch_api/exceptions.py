

class LaunchAPIException(Exception):
    def __init__(self, message, status_code):
        super(Exception, self).__init__(message)

        self.status_code = status_code


class ClientException(LaunchAPIException):
    pass
