import librosa

def extract_audio_segments(audio_path, segment_duration=1):

    y, sr = librosa.load(audio_path, sr=None)

    segment_length = int(sr * segment_duration)

    segments = []

    for i in range(0, len(y), segment_length):

        segment = y[i:i+segment_length]

        segments.append(segment.tobytes())

    return segments