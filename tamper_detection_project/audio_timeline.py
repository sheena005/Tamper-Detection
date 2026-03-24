def build_audio_timeline(total_segments, modified_segments):

    timeline = []

    for i in range(total_segments):

        if i in modified_segments:
            timeline.append((i, "TAMPERED"))
        else:
            timeline.append((i, "OK"))

    return timeline