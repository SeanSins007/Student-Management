# services/course_service.py

from models.course import Course
from storage.json_storage import JSONStorage
from utils.id_generator import generate_id
from utils.validators import validate_credits
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    heading, 
    # subheading
)

class CourseService:
    def __init__(self, storage_file="data/courses.json"):
        self.storage = JSONStorage(storage_file)
        info("CourseService initialized.")  # Informational

    def add_course(self, name: str, instructor: str, credits: int) -> Course | None:
        heading("Adding a new course")
        if not validate_credits(credits):
            warning(f"Credits out of valid range (1-10): {credits}")  # Warning for unusual input
            return None

        course_id = generate_id("C")
        course = Course(course_id, name, instructor, credits)
        self.storage.add(course)
        success(f"Course added successfully: {course}")  # Success message
        return course

    def get_all_courses(self):
        courses = self.storage.load(Course)
        info(f"{len(courses)} courses loaded.")  # Inform how many courses are retrieved
        return courses

    def find_course(self, course_id: str) -> Course | None:
        courses = self.get_all_courses()
        for course in courses:
            if course.course_id == course_id:
                info(f"Course found: {course}")  # Informational
                return course
        warning(f"Course not found with ID: {course_id}")  # Warning for missing course
        return None

    def update_course(self, course_id: str, name: str = None, instructor: str = None, credits: int = None):
        heading("Updating course")
        course = self.find_course(course_id)
        if not course:
            error(f"Cannot update. Course not found: {course_id}")  # Error message
            return None

        if name:
            course.name = name
            info(f"Name updated to: {name}")  # Informational

        if instructor:
            course.instructor_name = instructor
            info(f"Instructor updated to: {instructor}")  # Informational

        if credits is not None:
            if not validate_credits(credits):
                warning(f"Invalid credits provided: {credits}")  # Warning
                return None
            course.credits = credits
            info(f"Credits updated to: {credits}")  # Informational

        self.storage.update(course, key="course_id")
        success(f"Course updated successfully: {course}")  # Success
        return course

    def delete_course(self, course_id: str):
        heading("Deleting course")
        course = self.find_course(course_id)
        if not course:
            error(f"Cannot delete. Course not found: {course_id}")  # Error
            return

        self.storage.delete(course_id, Course, key="course_id")
        success(f"Course deleted successfully: {course_id}")  # Success
