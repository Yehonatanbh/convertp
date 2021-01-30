class BaseLoader:
    def load(self, payload):
        """
        converts the data given to raw audio data
        """
        raise NotImplementedError
