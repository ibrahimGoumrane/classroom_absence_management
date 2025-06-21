import os
import json
from PIL import Image
import random
from tqdm import tqdm


def create_classroom_picture(
    class_path, background_path, output_path, base_image_size=(100, 100), presence_prob=0.8, scale_factor=0.8
):
    """
    Create a classroom picture by placing student face images at desk positions on a background.
    Images are scaled based on row to simulate farness. Returns the list of included student IDs.

    Args:
        class_path (str): Path to the class folder containing student ID folders.
        background_path (str): Path to the classroom background image (880x523 pixels).
        output_path (str): Path to save the output class picture.
        base_image_size (tuple): Size of face images in the front row (width, height).
        presence_prob (float): Probability (0 to 1) of including a student's image.
        scale_factor (float): Scaling factor per row to simulate farness (e.g., 0.8 = 80% of previous row's size).

    Returns:
        list: List of student IDs included in the picture.
    """
    # Define desk positions (x, y coordinates) for a classroom with 4 seats in front row,
    # 6 seats in each of the 3 subsequent rows, fitted to 880x523 background
    desk_positions = [
        # Front row (4 seats)
        (60, 400),
        (280, 400),
        (500, 400),
        (720, 400),
        # Second row (6 seats)
        (30, 300),
        (160, 300),
        (320, 300),
        (480, 300),
        (620, 300),
        (760, 300),
        # Third row (6 seats)
        (100, 220),
        (220, 220),
        (340, 220),
        (460, 220),
        (580, 220),
        (700, 220),
        # Fourth row (6 seats)
        (200, 150),
        (280, 150),
        (360, 150),
        (450, 150),
        (520, 150),
        (600, 150),
    ]

    # Define scale factors for each row (front row = 1.0, each subsequent row scaled by scale_factor)
    row_scales = [
        1.0,  # Front row
        scale_factor,  # Second row
        scale_factor**2,  # Third row
        scale_factor**3,  # Fourth row
    ]

    # Assign scales to each desk position based on row
    desk_scales = [row_scales[0]] * 4 + [row_scales[1]] * 6 + [row_scales[2]] * 6 + [row_scales[3]] * 6

    # Load background image
    try:
        background = Image.open(background_path)
        if background.size != (880, 523):
            print(f"Warning: Background image size {background.size} does not match expected (880, 523)")
    except Exception as e:
        print(f"Error loading background image {background_path}: {e}")
        return []

    # List to store image paths and student IDs
    student_data = []

    # Walk through class folder to find student images
    for student_folder in os.listdir(class_path):
        student_path = os.path.join(class_path, student_folder)
        if os.path.isdir(student_path):
            # Look for image files in student folder
            for file in os.listdir(student_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    student_data.append({'id': student_folder, 'path': os.path.join(student_path, file)})

    if not student_data:
        print(f"No images found in {class_path}")
        return []

    # Shuffle student data to randomize placement
    random.shuffle(student_data)

    # Limit the number of students to the number of desk positions
    max_students = min(len(student_data), len(desk_positions))

    # List to store included student IDs
    included_students = []

    # Paste student images onto background
    for idx in range(max_students):
        # Apply presence probability (80% chance to include)
        if random.random() > presence_prob:
            continue

        student = student_data[idx]
        img_path = student['path']
        student_id = student['id']
        try:
            # Open image
            img = Image.open(img_path)

            # Calculate scaled size based on row
            scale = desk_scales[idx]
            scaled_size = (int(base_image_size[0] * scale), int(base_image_size[1] * scale))
            img = img.resize(scaled_size, Image.LANCZOS)

            # Get desk position
            x, y = desk_positions[idx]

            # Adjust position to center the scaled image
            x_offset = x + (base_image_size[0] - scaled_size[0]) // 2
            y_offset = y + (base_image_size[1] - scaled_size[1]) // 2

            # Paste image onto background
            background.paste(img, (x_offset, y_offset))
            included_students.append(student_id)
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    # Save the output image
    background.save(output_path)
    return included_students


if __name__ == "__main__":
    classes_path = "training"
    output_base_path = "gen_mock_data/classroom_pictures"
    background_path = "gen_mock_data/classroom_bg.jpeg"
    num_images_per_class = 5

    # Ensure output base directory exists
    os.makedirs(output_base_path, exist_ok=True)

    # Dictionary to store picture-to-student mappings for all classes
    all_class_mappings = {}

    # Get list of class folders
    class_folders = [f for f in os.listdir(classes_path) if os.path.isdir(os.path.join(classes_path, f))]

    # Iterate over class folders with progress bar
    for class_folder in tqdm(class_folders, desc="Processing classes"):
        class_path = os.path.join(classes_path, class_folder)

        # Create class-specific output directory
        class_output_path = os.path.join(output_base_path, class_folder)
        os.makedirs(class_output_path, exist_ok=True)

        # Dictionary to store picture-to-student mappings for this class
        class_mappings = {}

        # Generate 5 images for this class with progress bar
        for i in tqdm(range(num_images_per_class), desc=f"Generating images for {class_folder}", leave=False):
            output_filename = f"{class_folder}_picture_{i+1}.png"
            output_path = os.path.join(class_output_path, output_filename)

            # Generate picture and get included students
            included_students = create_classroom_picture(
                class_path,
                background_path,
                output_path,
                base_image_size=(100, 100),
                presence_prob=0.8,
                scale_factor=0.8,
            )

            # Store mapping
            class_mappings[output_filename] = included_students

        # Save class mappings to JSON
        json_path = os.path.join(class_output_path, f"{class_folder}_mappings.json")
        with open(json_path, 'w') as f:
            json.dump(class_mappings, f, indent=2)

        # Store in all_class_mappings
        all_class_mappings[class_folder] = class_mappings

    # Save a combined JSON for all classes
    combined_json_path = os.path.join(output_base_path, "all_class_mappings.json")
    with open(combined_json_path, 'w') as f:
        json.dump(all_class_mappings, f, indent=2)
