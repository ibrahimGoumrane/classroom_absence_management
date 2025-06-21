from pathlib import Path
import os
import pickle
from collections import Counter
from scipy.spatial.distance import euclidean
import face_recognition
from apps.students.models import Student
from apps.studentimages.models import StudentImage

DEFAULT_ENCODINGS_PATH = Path("encoding")
DEFAULT_TRAINING_PATH = Path('training')
DEFAULT_VALIDATION_PATH = Path('validation')

DEFAULT_TRAINING_PATH.mkdir(exist_ok=True)
DEFAULT_ENCODINGS_PATH.mkdir(exist_ok=True)
DEFAULT_VALIDATION_PATH.mkdir(exist_ok=True)


class imageException(Exception):
    def __init__(self, errorImage) -> None:
        super(imageException, self).__init__(errorImage)


class FaceRecognitionHandler:
    def __init__(self, encodings_location=DEFAULT_ENCODINGS_PATH):
        self.encodings_location = encodings_location
        self.model = "CNN"

    def __recognize_face(self, unknown_encoding, reference_encoding):
        boolean_matches = face_recognition.compare_faces(reference_encoding['encodings'], unknown_encoding)
        votes = Counter(name for match, name in zip(boolean_matches, reference_encoding["names"]) if match)
        if votes:
            name = votes.most_common(1)[0][0]
            ele_len = name.rfind('_encodings')
            return name[:ele_len]

    def __save_encodings(self, relative_path, filename, name_encodings):
        if not filename:
            return
        with Path(relative_path).joinpath(f"{filename}.pkl").open(mode="wb") as f:
            pickle.dump(name_encodings, f)

    def __handle_encodings(self, relative_path, filename, show_file_error=True):
        old_encodings = self.__load_encoded_faces(relative_path, filename, show_file_error == True)
        if old_encodings:
            return old_encodings
        return {'names': [], 'encodings': []}

    def __load_encoded_faces(self, relative_path, filename, show_file_error=True):
        try:
            with Path(relative_path).joinpath(f"{filename}.pkl").open(mode="rb") as f:
                loaded_encodings = pickle.load(f)
        except OSError as e:
            if show_file_error:
                print(f"An IOError occurred: {e}")
            return {'names': [], 'encodings': []}
        return loaded_encodings

    def __is_new_encoding(self, unique_encodings, new_encoding, threshold=0.5):
        for old_encoding in unique_encodings:
            if euclidean(old_encoding, new_encoding) < threshold:
                return False
        return True

    def encode_known_faces(self):
        """
        Encodes faces from new images (is_encoded=False) in the StudentImage model and saves them in the structure:
        encoding/class_name/student_id_encodings.pkl. Uses the Django StudentImage model to track processed images.
        """
        # Find students with at least one unencoded image
        students_with_new_images = Student.objects.filter(images__is_encoded=False).distinct()

        encoded_image_ids = []
        for student in students_with_new_images:
            # Get class name from student's section_promo
            the_classe = student.section_promo.name
            student_id = str(student.id)

            # Construct the encoding path: encoding/class_name/
            relative_path = os.path.join(self.encodings_location, the_classe)

            # Create directory if it doesn’t exist
            if not os.path.exists(relative_path):
                os.makedirs(relative_path)

            # Define the encoding filename
            filename = f"{student_id}_encodings"

            # Load existing encodings for this student (empty if none exist)
            face_encodings_old = self.__handle_encodings(relative_path, filename, show_file_error=False)

            # Get all unencoded images for this student
            new_images = student.images.filter(is_encoded=False)

            for student_image in new_images:
                # Load the image from its full path
                image_path = student_image.image.path
                image = face_recognition.load_image_file(image_path)

                # Detect face locations and generate encodings
                face_locations = face_recognition.face_locations(image, model=self.model)
                face_encodings = face_recognition.face_encodings(image, face_locations)

                # Add new encodings to the existing list
                for encoding in face_encodings:
                    if self.__is_new_encoding(face_encodings_old['encodings'], encoding):
                        face_encodings_old['encodings'].append(encoding)

                # Mark the image as encoded
                student_image.is_encoded = True
                student_image.save()
                
                # Add the image ID to the list
                encoded_image_ids.append(student_image.id)

            # Save the updated encodings for the student
            name_encodings = {"names": [filename], "encodings": face_encodings_old['encodings']}
            self.__save_encodings(relative_path, filename, name_encodings)
            
        return encoded_image_ids

    def recognize_faces(self, image_location, the_classe):
        """
        Recognizes faces in the given image by comparing against encodings for the specified class.
        Args:
            image_location: Path to the image to recognize faces in.
            the_classe: The class directory (e.g., "class_2024_b").
        Returns:
            List of recognized people (student IDs).
        """
        present_people = []
        input_image = face_recognition.load_image_file(image_location)
        input_face_locations = face_recognition.face_locations(input_image, model=self.model)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

        if not input_face_encodings:
            print('The image entered is not clear, enter a clear image to recognize face')
            raise imageException('Image not Clear')

        # Construct the relative path: encoding/the_classe/
        relative_path = os.path.join(DEFAULT_ENCODINGS_PATH, the_classe)

        # Iterate over all encoding files in the class directory
        for encoding_file in Path(relative_path).glob('*_encodings.pkl'):
            student_id = encoding_file.stem.replace('_encodings', '')  # Extract student_id from filename
            loaded_encodings = self.__load_encoded_faces(relative_path, encoding_file.stem)
            if not loaded_encodings['encodings']:
                print(f"No encodings found for {student_id} in {relative_path}")
                continue

            for unknown_encoding in input_face_encodings:
                searched_name = self.__recognize_face(unknown_encoding, loaded_encodings)
                if searched_name:
                    present_people.append(searched_name)
                    break

        return present_people


# Example usage
# face_handler = FaceRecognitionHandler()

# Encode faces with a custom subpath
# face_handler.encode_known_faces(subpath=['IAGI_PROMO_2027'])

# Recognize faces using the same subpath
# training_path = Path("validation/elon.jpg")
# print(face_handler.recognize_faces(training_path, 'IAGI_PROMO_2027'))
