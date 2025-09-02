import cv2
import numpy as np

def load_image(file):
    bytes_data = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(bytes_data, cv2.IMREAD_COLOR)
    return img

# Centering
def calculate_centering(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)
    
    # If detection fails, return None
    if coords is None:
        return None
    
    x, y, w, h = cv2.boundingRect(coords)
    h_img, w_img = gray.shape
    left, right = x, w_img - (x + w)
    top, bottom = y, h_img - (y + h)
    
    # Avoid division by zero
    if max(left, right) == 0 or max(top, bottom) == 0:
        return None
    
    horiz_ratio = min(left, right) / max(left, right)
    vert_ratio  = min(top, bottom) / max(top, bottom)
    
    return (horiz_ratio + vert_ratio) / 2
    return (horiz_ratio + vert_ratio) / 2

# Corners
def calculate_corners(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=4, qualityLevel=0.01, minDistance=10)
    if corners is None:
        return 1
    score = min(len(corners)/4, 1)
    return score

# Edges
def calculate_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    h, w = gray.shape
    border = 20
    border_edges = edges[:border,:].sum() + edges[-border:,:].sum() + edges[:,:border].sum() + edges[:,-border:].sum()
    score = 1 - border_edges / (border*2*(h+w))
    return np.clip(score, 0, 1)

# Surface
def calculate_surface(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    std = blur.std()
    return np.clip(1 - std/100, 0, 1)

# PSA
def evaluate_psa_centering(ratio):
    if ratio >= 0.55: return 10
    elif ratio >= 0.50: return 9
    elif ratio >= 0.45: return 8
    elif ratio >= 0.40: return 7
    elif ratio >= 0.35: return 6
    elif ratio >= 0.30: return 5
    elif ratio >= 0.25: return 4
    elif ratio >= 0.20: return 3
    elif ratio >= 0.15: return 2
    else: return 1

def evaluate_psa_subgrade(score):
    return max(1, min(10, int(score*10)))

# ACE
def evaluate_ace_centering(ratio):
    if ratio >= 0.60: return 10
    elif ratio >= 0.55: return 9
    elif ratio >= 0.50: return 8
    elif ratio >= 0.45: return 7
    elif ratio >= 0.40: return 6
    elif ratio >= 0.35: return 5
    elif ratio >= 0.30: return 4
    elif ratio >= 0.25: return 3
    else: return 2

def evaluate_ace_subgrade(score):
    return max(1, min(10, int(score*10)))

# Overall
def calculate_overall_grade(sub_grades):
    return min(sub_grades.values())

# Full Evaluation
def evaluate_card(front_file, back_file, grading_style):
    front = load_image(front_file)
    back = load_image(back_file)
    
    front_center = calculate_centering(front)
    back_center = calculate_centering(back)
    centering_ratio = (front_center + back_center)/2
    
    corners_ratio = min(calculate_corners(front), calculate_corners(back))
    edges_ratio = min(calculate_edges(front), calculate_edges(back))
    surface_ratio = min(calculate_surface(front), calculate_surface(back))
    
    if grading_style == "PSA":
        sub_grades = {
            "Centering": evaluate_psa_centering(centering_ratio),
            "Corners": evaluate_psa_subgrade(corners_ratio),
            "Edges": evaluate_psa_subgrade(edges_ratio),
            "Surface": evaluate_psa_subgrade(surface_ratio)
        }
    else:
        sub_grades = {
            "Centering": evaluate_ace_centering(centering_ratio),
            "Corners": evaluate_ace_subgrade(corners_ratio),
            "Edges": evaluate_ace_subgrade(edges_ratio),
            "Surface": evaluate_ace_subgrade(surface_ratio)
        }
    
    overall_grade = calculate_overall_grade(sub_grades)
    return overall_grade, sub_grades
