import os
from concurrent.futures import ThreadPoolExecutor

from utils_vbee import (
    load_api_key,
    send_tts_request,
    check_tts_status,
    download_audio_file,
)


def get_voice_tag(voice_code):
    parts = voice_code.split("_")
    # Extract the city abbreviation and gender
    city = parts[0].split("-")[0]
    gender = "f" if "female" in parts[1] else "m"
    # Combine them into the desired tag format
    voice_tag = f"{city}_{gender}"
    return voice_tag


def process_text(input_text, index, voice_codes, api_key):
    voice_code = voice_codes[index % len(voice_codes)]
    voice_tag = get_voice_tag(voice_code)
    speed_rate = 1.0

    print(f"Processing {index + 1}: {input_text}")
    response_data = send_tts_request(api_key, input_text, voice_code, speed_rate)

    if "result" in response_data and "request_id" in response_data["result"]:
        request_id = response_data["result"]["request_id"]
        try:
            audio_url = check_tts_status(api_key, request_id, len(input_text))
            local_audio_path = (
                f"wavs/universal3/audio_{index + 1}_{voice_tag}_{len(input_text)}.wav"
            )
            download_audio_file(audio_url, local_audio_path)
            print(f"Audio file saved: {local_audio_path}")
        except Exception as e:
            print(f"Failed to process text {index + 1}: {e}")
    else:
        print(
            f"Request ID not found for text {index + 1}. Here's the POST response: {response_data}"
        )


def main():
    api_key = load_api_key()

    voice_codes = [
        "hn_female_ngochuyen_full_48k-fhg",
        "hn_male_phuthang_news65dt_44k-fhg",
        "hn_male_manhdung_news_48k-fhg",
        "hn_male_thanhlong_talk_48k-fhg",
        "hn_female_maiphuong_vdts_48k-fhg",
        "sg_female_tuongvy_call_44k-fhg",
        "sg_female_lantrinh_vdts_48k-fhg",
        "sg_male_trungkien_vdts_48k-fhg",
        "sg_male_minhhoang_full_48k-fhg",
        "sg_female_thaotrinh_full_48k-fhg",
        "hue_male_duyphuong_full_48k-fhg",
        "hue_female_huonggiang_full_48k-fhg",
    ]

    with open("src/vi_universal_3.txt", "r", encoding="utf-8") as file:
        input_texts = [line.strip() for line in file.readlines() if line.strip()]

    # Adjust the range to start from index 205
    start_index = 0
    input_texts_subset = input_texts[start_index:]

    # Using ThreadPoolExecutor to manage multiple threads
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [
            executor.submit(process_text, text, idx + start_index, voice_codes, api_key)
            for idx, text in enumerate(input_texts_subset)
        ]

        # Wait for all futures to complete
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
