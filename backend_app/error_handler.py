from http import HTTPStatus


class ApiError(Exception):
    status_code = 400
    __name__ = "ApiError"

    def __init__(self, message=None, error=None, status_code=None):
        Exception.__init__(self)
        if isinstance(error, Exception):
            self.error_msg = str(error)
            try:
                self.error = type(error).__name__
            except:
                self.error = type(error)
        elif error:
            self.error = str(error)
        self.args = self.message = (message,)
        self.status_code = status_code

    def serialize(self):
        rv = dict(())
        if self.status_code:
            rv['status_code'] = str(self.status_code)
            rv['reply'] = HTTPStatus(self.status_code).phrase
        if hasattr(self, 'message'):
            rv['message'] = self.message
        if hasattr(self, 'error'):
            rv['error'] = self.error
            rv['error_message'] = self.error_msg
        return rv


class XMLParsingError(Exception):
    pass


class InternalError(Exception):
    pass


class SamlParsingError(Exception):
    pass


class FileUploadError(Exception):
    pass
