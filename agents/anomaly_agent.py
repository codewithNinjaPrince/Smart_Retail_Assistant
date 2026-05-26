import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AnomalyAgent:

    def __init__(self):

        self.endpoint=os.getenv(
            "AZURE_ANOMALY_ENDPOINT"
        )

        self.key=os.getenv(
            "AZURE_ANOMALY_KEY"
        )

    def detect(self,data):

        headers={

            "Ocp-Apim-Subscription-Key":
            self.key,

            "Content-Type":
            "application/json"
        }

        payload={

            "series":data,

            "granularity":"daily",

            "sensitivity":95
        }

        url=f"{self.endpoint}/anomalydetector/v1.1/timeseries/entire/detect"

        response=requests.post(
            url,
            headers=headers,
            json=payload
        )

        return response.json()