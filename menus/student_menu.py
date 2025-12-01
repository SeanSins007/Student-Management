# menus/student_menu.py

from services.report_service import ReportService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from utils.msg import (
    error, 
    # success, 
    info, 
    # warning, 
    heading, 
    subheading
    )


def run_student_menu(student):
    report_service = ReportService()
    course_service = CourseService()
    enrollment_service = EnrollmentService()

    def list_courses(courses):
        if not courses:
            info("No courses available.")
            return
        heading("=== Courses ===")
        for c in courses:
            teacher_info = f" | Teacher: {c.teacher_id}" if getattr(c, 'teacher_id', None) else ""
            info(f"ID: {c.course_id} | Name: {c.name} | Credits: {c.credits}{teacher_info}")

    while True:
        heading(f"\n=== Student Menu ({student.name}) ===")
        print(subheading("1. View My Profile"))
        print(subheading("2. View Available Courses"))
        print(subheading("3. Enroll in a Course"))
        print(subheading("4. View My Enrollments / Grades"))
        print(subheading("5. Logout"))
        
        info("Enter choice: ")
        choice = input().strip()

        # ---------------- Profile ----------------
        if choice == "1":
            heading("\n=== My Profile ===")
            info(str(student))

        # ---------------- View Courses ----------------
        elif choice == "2":
            courses = course_service.get_all_courses()
            list_courses(courses)

        # ---------------- Enroll ----------------
        elif choice == "3":
            courses = course_service.get_all_courses()
            list_courses(courses)
            course_id = input(subheading("Enter Course ID to enroll (or press Enter to cancel): ")).strip()
            if not course_id:
                continue
            success = enrollment_service.enroll(student.student_id, course_id)
            if success:
                success(f"Successfully enrolled in course {course_id}.")
            else:
                error(f"Failed to enroll in course {course_id}. Check if the ID is correct or already enrolled.")

        # ---------------- View Enrollments / Grades ----------------
        elif choice == "4":
            enrollments = enrollment_service.get_student_enrollments(student.student_id)
            if not enrollments:
                info("You are not enrolled in any courses.")
            else:
                heading("=== My Enrollments / Grades ===")
                for e in enrollments:
                    grade = getattr(e, 'grade', 'N/A')
                    course_name = getattr(e, 'course_name', 'Unknown Course')
                    info(f"Course ID: {e.course_id} | Name: {course_name} | Grade: {grade}")
        # ---------------- Logout ----------------
        elif choice == "5":
            info("Logging out...")
            break

        else:
            error("Invalid choice. Please select a valid option.")