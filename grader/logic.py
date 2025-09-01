# grader/logic.py
import cv2
import numpy as np

def evaluate_card(front_file, back_file):
    """
    Simple grading logic using image heuristics.
    Returns a predicted grade string.
    """

    def load_image(file):
        # Convert uploaded file to OpenCV image
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return img

    def score_centering(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        coords = cv2.findNonZero(thresh)
        if coords is None:
            return 0.5  # fallback
        x, y, w, h = cv2.boundingRect(coords)
        cx, cy = x + w / 2, y + h / 2
        h_img, w_img = gray.shape
        centering_score = 1 - (abs(cx - w_img/2)/(w_img/2) + abs(cy - h_img/2)/(h_img/2)) / 2
        return np.clip(centering_score, 0, 1)

    front_img = load_image(front_file)
    back_img = load_image(back_file)

    # Compute simple centering score for both sides
    centering_front = score_centering(front_img)
    centering_back = score_centering(back_img)

    # Average and map to grade (simple scale 6–10)
    avg_score = (centering_front + centering_back) / 2
    grade = 6 + 4 * avg_score
    return f"Predicted Grade: {grade:.1f}"
