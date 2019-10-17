class ErrorHandler:
    @classmethod
    def process_error(cls, error):
        cls.error = error
        return cls.error
