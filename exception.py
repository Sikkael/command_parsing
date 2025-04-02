class AuthenticationError(Exception):
    """Exception raised for errors in authentication.

    Attributes:
        self.error_flag -- the error number
        message -- explanation of the error
    """

    def __init__(self, error_flag):
        self.error_flag = error_flag
        if self.error_flag == -504:
            self.message = "Access denied"
        else:
            self.message = "Login failed"

        super().__init__(self.message)

    def __str__(self):
        return f'{self.error_flag} -> {self.message}'


class FileStoreError(Exception):
    """Exception raised for errors in file encryption & decryption.
       Example: file is missing

        Attributes:

            message -- explanation of the error
        """

    def __init__(self, message):
        self.message = message

        super().__init__(self.message)

