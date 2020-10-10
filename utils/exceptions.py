class NotFittedError(ValueError, AttributeError):
    pass

class MissingFeatureError(ValueError, AttributeError):
    pass