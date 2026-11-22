"""
Crowd density estimation module.

Runs on video FRAMES from public/sample datasets or pre-recorded footage —
never on a live camera. Uses OpenCV's built-in HOG + Linear SVM people
detector, which ships with opencv-python (no external weight download
required), so this module works fully offline.

For higher accuracy in a production setting this function can be swapped
for a YOLOv8 person-detection model (see README) without changing the
rest of the pipeline — it only needs to keep returning an integer count.
"""
import cv2
import numpy as np


_hog = cv2.HOGDescriptor()
_hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def count_people_in_frame(frame: np.ndarray) -> int:
    """
    Detect and count people in a single BGR image frame.

    Args:
        frame: an OpenCV BGR image (numpy array), e.g. from a sample
               dataset video read via cv2.VideoCapture.

    Returns:
        Estimated number of people detected in the frame.
    """
    if frame is None or frame.size == 0:
        return 0

    # Downscale for speed/consistency on varying dataset resolutions
    h, w = frame.shape[:2]
    scale = 640 / max(w, 1)
    if scale < 1.0:
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

    rects, weights = _hog.detectMultiScale(
        frame, winStride=(8, 8), padding=(8, 8), scale=1.05
    )
    return len(rects)


def estimate_capacity_pct(person_count: int, expected_capacity: int) -> float:
    """Convert a raw person count into a % of expected safe capacity."""
    if expected_capacity <= 0:
        return 0.0
    return round(min(person_count / expected_capacity, 3.0) * 100, 1)


def count_people_in_video_sample(video_path: str, sample_every_n_frames: int = 15):
    """
    Utility for batch-processing a downloaded sample/public platform video
    dataset and yielding (frame_index, person_count) tuples. Intended to be
    called from the simulator, not from a live API request.
    """
    cap = cv2.VideoCapture(video_path)
    idx = 0
    results = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx % sample_every_n_frames == 0:
            count = count_people_in_frame(frame)
            results.append((idx, count))
        idx += 1
    cap.release()
    return results
