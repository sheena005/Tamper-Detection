import cv2

def get_frame(video_path, frame_number):

    cap = cv2.VideoCapture(video_path)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    ret, frame = cap.read()

    cap.release()

    if ret:
        return frame

    return None