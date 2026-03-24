def build_video_timeline(total_frames, modified_frames):

    timeline = []

    for i in range(total_frames):

        if i in modified_frames:
            timeline.append((i, "TAMPERED"))
        else:
            timeline.append((i, "OK"))

    return timeline