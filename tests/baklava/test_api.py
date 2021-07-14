import os
import baklava


def sample():
    directory = os.path.dirname(__file__)
    return os.path.join(directory, "sample")


def test_predict():
    result = baklava.predict(sample(), ["--help"])
    assert result == 0


def test_train():
    result = baklava.predict(sample(), ["--help"])
    assert result == 0


if __name__ == '__main__':
    test_predict()
    test_train()
