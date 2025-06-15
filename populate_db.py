"""
How to run:
python manage.py shell
>>> exec(open('populate_db.py').read())
"""

from apps.attendance.models import Attendance
from apps.classes.models import Class
from apps.departments.models import Department
from apps.studentimages.models import StudentImage
from apps.students.models import Student
from apps.subjects.models import Subject
from apps.teachers.models import Teacher
from apps.users.models import User
from django.utils.timezone import make_aware
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
import uuid
import requests
import os
import random
from tqdm import tqdm

# Create 1 admin account
print("Creating 1 admin...")
admin_data = {
    'email': 'admin@example.com',
    'firstName': 'Admin',
    'lastName': 'User',
    'password': 'adminpass',
    'role': 'admin',
}
admin, created = User.objects.get_or_create(
    email=admin_data['email'],
    defaults={
        'firstName': admin_data['firstName'],
        'lastName': admin_data['lastName'],
        'role': admin_data['role'],
        'is_staff': True,
        'is_superuser': True,
    },
)
if created or not admin.password:
    admin.set_password(admin_data['password'])
    admin.save()

# Create 6 departments with descriptions
print("Creating 6 departments...")
departments_data = [
    {'name': 'Mathematics', 'description': 'Focuses on numbers, algebra, calculus, and geometry.'},
    {'name': 'Physics', 'description': 'Studies energy, matter, mechanics, and electromagnetism.'},
    {'name': 'Computer Science', 'description': 'Explores programming, algorithms, and data structures.'},
    {'name': 'Biology', 'description': 'Investigates living organisms, genetics, and ecology.'},
    {'name': 'Chemistry', 'description': 'Examines chemical reactions and material properties.'},
    {'name': 'Engineering', 'description': 'Applies science to design systems and structures.'},
]
for data in tqdm(departments_data, desc="Departments"):
    Department.objects.get_or_create(name=data['name'], defaults={'description': data['description']})

# Create 22 teacher users and teachers
print("Creating 22 teachers...")
teacher_users = [
    {
        'email': f'teacher{i}@example.com',
        'firstName': f'Teacher{i}',
        'lastName': f'TUser{i}',
        'role': 'teacher',
        'password': f'teacherpass{i}',
    }
    for i in range(1, 23)
]
departments = list(Department.objects.all().order_by('id'))
for user_data in tqdm(teacher_users, desc="Teachers"):
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={
            'firstName': user_data['firstName'],
            'lastName': user_data['lastName'],
            'role': user_data['role'],
        },
    )
    if created or not user.password:
        user.set_password(user_data['password'])
        user.save()
    dept = departments[teacher_users.index(user_data) % len(departments)]
    Teacher.objects.get_or_create(user=user, defaults={'department': dept})

# Create 12 classes
print("Creating 12 classes...")
classes_data = [
    {'name': 'Mathematics 101'},
    {'name': 'Mathematics 102'},
    {'name': 'Physics 201'},
    {'name': 'Physics 202'},
    {'name': 'Computer Science 301'},
    {'name': 'Computer Science 302'},
    {'name': 'Biology 401'},
    {'name': 'Biology 402'},
    {'name': 'Chemistry 501'},
    {'name': 'Chemistry 502'},
    {'name': 'Engineering 601'},
    {'name': 'Engineering 602'},
]
for data in tqdm(classes_data, desc="Classes"):
    Class.objects.get_or_create(name=data['name'])

# Create 222 student users
print("Creating 222 students users...")
student_users = [
    {
        'email': f'student{i}@example.com',
        'firstName': f'Student{i}',
        'lastName': f'SUser{i}',
        'role': 'student',
        'password': f'studentpass{i}',
    }
    for i in range(1, 223)
]
for user_data in tqdm(student_users, desc="Student Users"):
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={
            'firstName': user_data['firstName'],
            'lastName': user_data['lastName'],
            'role': user_data['role'],
        },
    )
    if created or not user.password:
        user.set_password(user_data['password'])
        user.save()

# Create 222 students, linking to users and classes (~18-19 per class)
users = list(User.objects.filter(role='student').order_by('id'))
classes = list(Class.objects.all().order_by('id'))
students_per_class = [18] * 6 + [19] * 6  # Distribute: 6 classes with 18, 6 with 19
random.shuffle(students_per_class)
student_count = 0
print("Assigning students to classes...")
for cls, num_students in tqdm(
    zip(classes, students_per_class), total=len(classes), desc="Students to Classes"
):
    for i in range(num_students):
        user = users[student_count]
        Student.objects.get_or_create(user=user, defaults={'section_promo': cls})
        student_count += 1

# Create student images
print("Fetching and creating student images (AI-generated faces)...")
students = Student.objects.all()
for student in tqdm(students, desc="Student Images"):
    class_name = student.section_promo.name
    unique_filename = f"{uuid.uuid4().hex}.jpg"
    # Fetch AI-generated face image from ThisPersonDoesNotExist
    response = requests.get("https://thispersondoesnotexist.com")
    if response.status_code == 200:
        # Define the image path relative to MEDIA_ROOT
        image_path = os.path.join(class_name, str(student.id), unique_filename)
        # Create a StudentImage instance
        student_image, created = StudentImage.objects.get_or_create(
            student=student, image=image_path, defaults={'is_encoded': False}
        )
        if created:
            # Save the image content to the image field
            student_image.image.save(unique_filename, ContentFile(response.content))

# Create 30 subjects linked to teachers and classes
print("Creating 30 subjects...")
teachers = list(Teacher.objects.all().order_by('id'))
classes = list(Class.objects.all().order_by('id'))
subjects_data = [
    {'name': 'Algebra', 'teacher': teachers[0], 'section_promo': classes[0]},  # Mathematics 101
    {'name': 'Calculus', 'teacher': teachers[1], 'section_promo': classes[0]},
    {'name': 'Linear Algebra', 'teacher': teachers[2], 'section_promo': classes[0]},
    {'name': 'Geometry', 'teacher': teachers[3], 'section_promo': classes[1]},  # Mathematics 102
    {'name': 'Number Theory', 'teacher': teachers[4], 'section_promo': classes[1]},
    {'name': 'Mechanics', 'teacher': teachers[5], 'section_promo': classes[2]},  # Physics 201
    {'name': 'Quantum Mechanics', 'teacher': teachers[6], 'section_promo': classes[2]},
    {'name': 'Electromagnetism', 'teacher': teachers[7], 'section_promo': classes[3]},  # Physics 202
    {'name': 'Optics', 'teacher': teachers[8], 'section_promo': classes[3]},
    {'name': 'Programming', 'teacher': teachers[9], 'section_promo': classes[4]},  # Computer Science 301
    {'name': 'Data Structures', 'teacher': teachers[10], 'section_promo': classes[4]},
    {'name': 'Algorithms', 'teacher': teachers[11], 'section_promo': classes[5]},  # Computer Science 302
    {'name': 'Databases', 'teacher': teachers[12], 'section_promo': classes[5]},
    {'name': 'Genetics', 'teacher': teachers[13], 'section_promo': classes[6]},  # Biology 401
    {'name': 'Ecology', 'teacher': teachers[14], 'section_promo': classes[7]},  # Biology 402
    {'name': 'Microbiology', 'teacher': teachers[15], 'section_promo': classes[7]},
    {'name': 'Organic Chemistry', 'teacher': teachers[16], 'section_promo': classes[8]},  # Chemistry 501
    {'name': 'Inorganic Chemistry', 'teacher': teachers[17], 'section_promo': classes[8]},
    {'name': 'Analytical Chemistry', 'teacher': teachers[18], 'section_promo': classes[8]},
    {'name': 'Physical Chemistry', 'teacher': teachers[19], 'section_promo': classes[9]},  # Chemistry 502
    {'name': 'Biochemistry', 'teacher': teachers[20], 'section_promo': classes[9]},
    {'name': 'Thermodynamics', 'teacher': teachers[21], 'section_promo': classes[10]},  # Engineering 601
    {'name': 'Structural Engineering', 'teacher': teachers[0], 'section_promo': classes[10]},
    {'name': 'Fluid Mechanics', 'teacher': teachers[1], 'section_promo': classes[10]},
    {'name': 'Circuit Design', 'teacher': teachers[2], 'section_promo': classes[11]},  # Engineering 602
    {'name': 'Robotics', 'teacher': teachers[3], 'section_promo': classes[11]},
    {'name': 'Control Systems', 'teacher': teachers[4], 'section_promo': classes[11]},
    {'name': 'Statistics', 'teacher': teachers[5], 'section_promo': classes[1]},  # Mathematics 102
    {'name': 'Astrophysics', 'teacher': teachers[6], 'section_promo': classes[2]},  # Physics 201
    {'name': 'Software Engineering', 'teacher': teachers[7], 'section_promo': classes[4]},  # Computer Science 301
]
for data in tqdm(subjects_data, desc="Subjects"):
    Subject.objects.get_or_create(
        name=data['name'], teacher=data['teacher'], section_promo=data['section_promo']
    )


# Automate attendance records
print("Creating attendance records...")


def get_weekday_offsets(start_date, num_days):
    """Generate a list of day offsets for weekdays (Mon-Fri) starting from start_date."""
    offsets = []
    current_date = start_date
    count = 0
    while count < num_days:
        if current_date.weekday() < 5:  # 0=Mon, 1=Tue, ..., 4=Fri
            offsets.append(count)
            count += 1
        current_date += timedelta(days=1)
    return offsets


classes = Class.objects.all()
start_date = datetime(2025, 5, 1)
num_days = 60
hours = [9, 11, 15, 17]  # Possible hours for subject sessions (hour within the session)
weekday_offsets = get_weekday_offsets(start_date, num_days)
for cls in tqdm(classes, desc="Classes"):
    subjects = list(Subject.objects.filter(section_promo=cls))  # Convert to list for random.choice
    students = Student.objects.filter(section_promo=cls)
    for day_offset in tqdm(weekday_offsets, desc=f"Days for {cls.name}", leave=False):
        # Randomly select 1–3 session times for the class on this day
        num_sessions = random.randint(1, 3)
        session_hours = random.sample(hours, num_sessions)  # Unique hours
        for hour in session_hours:
            if subjects:
                subject = random.choice(subjects)
                current_date = start_date.replace(hour=hour, minute=0, second=0) + timedelta(days=day_offset)
                for student in students:
                    status = random.choices(['present', 'absent'], weights=[0.8, 0.2], k=1)[0]
                    Attendance.objects.get_or_create(
                        student=student,
                        subject=subject,
                        date=make_aware(current_date),
                        defaults={'status': status},
                    )
