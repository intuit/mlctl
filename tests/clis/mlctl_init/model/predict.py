import functools

@functools.lru_cache()
def init(pa):
    """
    Load the pickled model back into memory. Since loading models can be
    expensive, this function is cached so that the model only needs to be loaded
    into memory once.
    Returns:
        model (sklearn.tree.DecisionTreeClassifier): The trained decision tree.
    """


def predict(pa, payload):
    """
    Run the decision tree classifier on the input payload. It is expected that
    the payload will have an 'age' and 'height' key, otherwise an error will
    occur.
    Note: This is the prediction entrypoint used by baklava!
    Arguments:
        payload (dict[str, object]): This is the payload that will eventaully
            be sent to the server using a POST request.
    Returns:
        payload (dict[str, object]): The output of the function is expected to
            be either a dictionary (like the function input) or a JSON string.
    """