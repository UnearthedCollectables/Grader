import cv2
import numpy as np

def load_image(file):
    bytes_data = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(bytes_data, cv2.IMREAD_COLOR)
    return img

# Placeholder metric calculators (to be refined)
def calculate_centering(front, back):
    return (0.55, 0.75)

def calculate_corners(front, back):
    return (0.9, 0.9)

def calculate_edges(front, back):
    return (0.9, 0.9)

def calculate_surface(front, back):
    return (0.9, 0.9)

def evaluate_psa_centering(ratios):
    front, back = ratios
    if front <= 0.55 and back <= 0.75: return "10"
    elif front <= 0.60 and back <= 0.75: return "9"
    elif front <= 0.65 and back <= 0.75: return "8"
    elif front <= 0.70 and back <= 0.80: return "7"
    elif front <= 0.75 and back <= 0.80: return "6"
    elif front <= 0.80 and back <= 0.80: return "5"
    elif front <= 0.85 and back <= 0.85: return "4"
    elif front <= 0.90 and back <= 0.90: return "3"
    elif front <= 0.95 and back <= 0.95: return "2"
    else: return "1"

def evaluate_psa_corners(score):
    return str(int(score*10))

def evaluate_psa_edges(score):
    return str(int(score*10))

def evaluate_psa_surface(score):
    return str(int(score*10))

def evaluate_ace_centering(ratios):
    front, back = ratios
    if front <= 0.60 and back <= 0.75: return "10"
    elif front <= 0.65 and back <= 0.70: return "9"
    elif front <= 0.70 and back <= 0.75: return "8"
    elif front <= 0.75 and back <= 0.80: return "7"
    elif front <= 0.80 and back <= 0.80: return "6"
    elif front <= 0.80 and back <= 0.80: return "5"
    elif front <= 0.80 and back <= 0.80: return "4"
    elif front <= 0.85 and back <= 0.85: return "3"
    else: return "2"

def evaluate_ace_corners(score):
    return str(int(score*10))

def evaluate_ace_edges(score):
    return str(int(score*10))

def evaluate_ace_surface(score):
    return str(int(score*10))

def calculate_overall_grade(sub_grades):
    return min(sub_grades.values())

def evaluate_card(front_file, back_file, grading_style):
    front = load_image(front_file)
    back = load_image(back_file)
    centering = calculate_centering(front, back)
    corners = calculate_corners(front, back)
    edges = calculate_edges(front, back)
    surface = calculate_surface(front, back)

    if grading_style == "PSA":
        sub_grades = {
            "Centering": evaluate_psa_centering(centering),
            "Corners": evaluate_psa_corners(corners[0]),
            "Edges": evaluate_psa_edges(edges[0]),
            "Surface": evaluate_psa_surface(surface[0])
        }
    else:
        sub_grades = {
            "Centering": evaluate_ace_centering(centering),
            "Corners": evaluate_ace_corners(corners[0]),
            "Edges": evaluate_ace_edges(edges[0]),
            "Surface": evaluate_ace_surface(surface[0])
        }

    overall_grade = calculate_overall_grade(sub_grades)
    return overall_grade, sub_grades
