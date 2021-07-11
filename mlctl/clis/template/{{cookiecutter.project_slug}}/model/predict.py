import json


def predict(payload):
    """
    Define a hosted function that runs the model.
    Arguments:
        payload (dict[str, object]): This is the payload that is sent to the
            SageMaker server using a POST request to the `invocations` route.
    Returns:
        payload (dict[str, object]): The output of the function is expected to
            be either a dictionary (like the function input) or a JSON string.
    """

    payload = payload["data"]

    print(
        "You can print things for debugging"
    )

    return json.dumps(payload)