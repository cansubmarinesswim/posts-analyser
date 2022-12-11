import requests


class MlConnectorError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400
        self.message = message


class MlConnector:
    def __init__(self, host: str, port: str):
        self._host = host
        self._port = port

    def classify_post(self, text: str):
        try:
            print(text)
            response = requests.post(
                f"http://{self._host}:{self._port}/classify", data={"text": text}
            )
            return self._parse_classification_response(response)
        except Exception as e:
            raise MlConnectorError(e)

    def _parse_classification_response(self, response):
        json_response = response.json()
        formatted_json_response = {
            "positive": json_response[0][1],
            "neutral": json_response[1][1],
            "negative": json_response[2][1],
        }
        return formatted_json_response
