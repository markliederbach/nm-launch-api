import json


class MockResponse:
    def __init__(self, data=None, status_code=None, reason=None, is_ok=None, headers=None, text=None):
        assert data is not None or text is not None, "Must specify at least one response body object"
        self.data = data
        self.status_code = status_code if status_code is not None else 200
        self.reason = reason
        self.ok = bool(is_ok.lower() == 'true') if is_ok is not None else True
        self.headers = headers if headers is not None else {'content-type': 'application/json'}
        self._text = text if text is not None else json.dumps(self.data)

    @property
    def text(self):
        return self._text

    def json(self):
        return self.data
