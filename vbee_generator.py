import os

from utils_vbee import (
    load_api_key,
    send_tts_request,
    check_tts_status,
    download_audio_file,
)


def main():
    api_key = load_api_key()
    # print("API Key:", api_key)

    voice_codes = [
        "hn_female_ngochuyen_fast_news_48k-thg",
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

    with open("random_vietnamese_texts_1000.txt", "r", encoding="utf-8") as file:
        input_texts = file.readlines()

    # Loop through each text, send request, check status, and save audio
    for index, input_text in enumerate(input_texts):
        input_text = input_text.strip()
        if not input_text:
            continue

        voice_code = voice_codes[index % len(voice_codes)]
        speed_rate = 1.0

        print(f"Processing {index + 1}/{len(input_texts)}: {input_text}")
        response_data = send_tts_request(api_key, input_text, voice_code, speed_rate)

        if "result" in response_data and "request_id" in response_data["result"]:
            request_id = response_data["result"]["request_id"]
            try:
                audio_url = check_tts_status(api_key, request_id, len(input_text))
                local_audio_path = f"vbee/universal/audio{index + 1}.wav"
                download_audio_file(audio_url, local_audio_path)
                print(f"Audio file saved: {local_audio_path}")
            except Exception as e:
                print(f"Failed to process text {index + 1}: {e}")
        else:
            print(
                f"Request ID not found for text {index + 1}. Here's the POST response: {response_data}"
            )


if __name__ == "__main__":
    main()
