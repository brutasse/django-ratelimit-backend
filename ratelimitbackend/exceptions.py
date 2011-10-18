class RateLimitException(Exception):
    def __init__(self, msg, counts):
        self.counts = counts
        super(RateLimitException, self).__init__(msg)
