import time
import os
import requests
from dotenv import load_dotenv


def load_api_key():
    load_dotenv()
    return os.getenv("VBEE_API_KEY")


def send_tts_request(api_key, input_text, voice_code, speed_rate):
    post_url = "https://vbee.vn/api/v1/tts"
    payload = {
        "app_id": "20aead61-13a3-4e2c-a0d8-096231eb3cc7",
        "response_type": "indirect",
        "callback_url": "https://mydomain/callback",
        "input_text": input_text,
        "voice_code": voice_code,
        "audio_type": "wav",
        "bitrate": 128,
        "speed_rate": speed_rate,
        "sample_rate": 22050,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(post_url, headers=headers, json=payload, timeout=10)
    return response.json()


def check_tts_status(api_key, request_id, input_text_length):
    get_url = f"https://vbee.vn/api/v1/tts/{request_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    # Calculate initial wait time based on the number of characters in the input text
    initial_wait_time = input_text_length * 0.025
    print(
        f"Waiting {initial_wait_time} seconds before starting to poll for TTS status."
    )
    time.sleep(initial_wait_time)  # Initial delay before starting the polling

    for _ in range(20):  # Maximum number of retries
        time.sleep(1)  # Wait for 1 second before each check
        response = requests.get(get_url, headers=headers, timeout=10)
        response_data = response.json()
        if "result" in response_data and "status" in response_data["result"]:
            if response_data["result"]["status"] == "SUCCESS":
                return response_data["result"]["audio_link"]
            elif response_data["result"]["status"] == "FAILED":
                raise Exception("Text-to-Speech conversion failed.")
        else:
            continue
    raise Exception("Failed to complete the operation within the allowed retries.")


def download_audio_file(url, path):
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"Audio saved successfully at {path}")
    else:
        raise Exception(
            f"Failed to download the audio file: Status Code {response.status_code}"
        )
