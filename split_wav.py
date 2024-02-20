from pydub import AudioSegment
import os


def is_silence_chunk(dB_levels, min_len=500, max_len=5000, avg_dB_thresh=-20):
    """Check if the dB level list represents a silence chunk."""
    duration = len(dB_levels) * 1  # Assuming 1 ms per dB level for simplicity
    if not min_len <= duration <= max_len:
        return False
    avg_dB = sum(dB_levels) / len(dB_levels)
    return avg_dB < avg_dB_thresh


def segment_chunks(speech_chunks, min_length=4000, max_length=15000):
    """Segment or merge speech chunks to ensure they are within 5s to 15s."""
    segmented_chunks = []
    for start, end in speech_chunks:
        chunk_length = end - start
        if chunk_length < min_length:
            if (
                segmented_chunks
                and (segmented_chunks[-1][1] - segmented_chunks[-1][0] + chunk_length)
                <= max_length
            ):
                # Merge with the previous chunk if the total length is within the limit
                prev_start, prev_end = segmented_chunks.pop()
                segmented_chunks.append((prev_start, end))
            else:
                # If it cannot be merged, adjust to minimum length or leave as is
                # This could involve either leaving short chunks or extending them slightly
                # Decision may depend on application-specific requirements
                segmented_chunks.append((start, end))  # Adjust this logic as needed
        elif chunk_length > max_length:
            # Segment long chunks into smaller ones
            for segment_start in range(start, end, max_length):
                segment_end = min(segment_start + max_length, end)
                segmented_chunks.append((segment_start, segment_end))
        else:
            # Chunk is within the desired range
            segmented_chunks.append((start, end))
    return segmented_chunks


def extract_speech_chunks(
    file_path,
    output_folder,
    output_file_name,
    min_silence_len=500,
    silence_thresh=-25,
    min_length=4000,
    max_length=15000,
):
    audio = AudioSegment.from_file(file_path)
    silence_start = None
    dB_levels = []
    speech_chunks = []
    last_speech_end = 0

    for i in range(0, len(audio), 1):  # Analyze every 1 ms
        segment = audio[i : i + 1]
        dB = segment.dBFS

        if dB < silence_thresh:  # Potential silence
            if silence_start is None:  # Mark the start of a silence segment
                silence_start = i
            dB_levels.append(dB)
        else:
            if silence_start is not None:
                # Evaluate the potential silence chunk
                if is_silence_chunk(
                    dB_levels, min_len=min_silence_len, avg_dB_thresh=silence_thresh
                ):
                    # If it's silence, save the previous speech chunk
                    if last_speech_end < silence_start:
                        speech_chunks.append((last_speech_end, silence_start))
                    last_speech_end = i
                # Reset for next potential silence segment
                silence_start = None
                dB_levels = []

    # Check for a final speech chunk
    if last_speech_end < len(audio):
        speech_chunks.append((last_speech_end, len(audio)))

    # Segment or merge speech chunks to ensure they fit within the desired length range
    speech_chunks = segment_chunks(
        speech_chunks, min_length=min_length, max_length=max_length
    )

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Export the speech chunks
    for index, (start, end) in enumerate(speech_chunks, start=1):
        if index == 1:
            # For the first chunk, extend the end by 200 but don't change the start
            chunk = audio[start + 6000 : end + 300]
        elif index == len(speech_chunks):
            # For the last chunk, extend the start by 200 but don't extend the end
            chunk = audio[start - 300 : end]
        else:
            # For all other chunks, extend both start and end by 200
            chunk = audio[start - 300 : end + 300]

        chunk_name = os.path.join(
            output_folder, f"{output_file_name}_chunk_{index}.wav"
        )
        chunk.export(chunk_name, format="wav")
        print(f"Exported {chunk_name}")


FILE_NAME = "obama3"

extract_speech_chunks(f"./audio/{FILE_NAME}_converted.wav", "./split", f"{FILE_NAME}")
