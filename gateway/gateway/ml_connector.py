import requests

class MlConnectorError(Exception):
    def __init__(self, message):            
        super().__init__(message)
        self.status_code = 400

class MlConnector:
    def __init__(self, service_host: str, service_port:str):
        self.service_host = service_host
        self.service_port = service_port

    def classify_post(self, text: str):
        try:
            response = requests.post(
                f"http://{self.service_host}:{self.service_port}/classify",
                data={"text": text}
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