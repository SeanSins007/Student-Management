# analysis/stats.py

import pandas as pd
import numpy as np
from storage.json_storage import JSONStorage
from models.student import Student
from models.course import Course
from models.enrollment import Enrollment
from scipy import stats

class Stats:
    def __init__(self):
        self.student_storage = JSONStorage("data/students.json")
        self.course_storage = JSONStorage("data/courses.json")
        self.enrollment_storage = JSONStorage("data/enrollments.json")

    def student_count(self):
        students = self.student_storage.load(Student)
        return len(students)

    def course_count(self):
        courses = self.course_storage.load(Course)
        return len(courses)

    def average_grade(self):
        enrollments = self.enrollment_storage.load(Enrollment)
        grades = [e.grade for e in enrollments if e.grade is not None]
        if not grades:
            return None
        return np.mean(grades)

    def grade_distribution(self):
        enrollments = self.enrollment_storage.load(Enrollment)
        grades = [e.grade for e in enrollments if e.grade is not None]
        if not grades:
            return None
        return pd.Series(grades).value_counts().sort_index()

    def grade_statistics(self):
        """Returns mean, median, mode, std deviation of grades"""
        enrollments = self.enrollment_storage.load(Enrollment)
        grades = [e.grade for e in enrollments if e.grade is not None]
        if not grades:
            return None
        mean = np.mean(grades)
        median = np.median(grades)
        mode = stats.mode(grades).mode[0] if grades else None
        std = np.std(grades)
        return {"mean": mean, "median": median, "mode": mode, "std_dev": std}
