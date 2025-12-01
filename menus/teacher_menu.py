# menus/teacher_menu.py

from services.enrollment_service import EnrollmentService
from services.course_service import CourseService
from services.report_service import ReportService
from utils.msg import (
    error, 
    success, 
    info, 
    # warning, 
    heading, 
    subheading
    )

def run_teacher_menu(teacher):
    """
    Teacher Menu:
    - teacher: Teacher object (must have .name and .teacher_id)
    - Courses are linked by teacher_id in Course objects.
    """
    enrollment_service = EnrollmentService()
    course_service = CourseService()
    report_service = ReportService()

    def list_courses(courses):
        if not courses:
            info("No courses assigned to you.")
            return
        heading("=== My Courses ===")
        for c in courses:
            info(f"ID: {c.course_id} | Name: {c.name} | Credits: {c.credits}")
    def list_enrollments(enrollments, courses_map):
        if not enrollments:
            info("No enrollments for your courses.")
            return
        heading("=== Enrollments ===")
        for e in enrollments:
            course_name = courses_map.get(e.course_id, "Unknown Course")
            grade = getattr(e, 'grade', 'N/A')
            info(f"Enrollment ID: {e.enrollment_id} | Student ID: {e.student_id} | Course: {course_name} | Grade: {grade}")
    while True:
        heading(f"\n=== Teacher Menu ({teacher.name}) ===")
        print(subheading("1. View My Profile"))
        print(subheading("2. View Courses I Teach"))
        print(subheading("3. View Enrollments for My Courses"))
        print(subheading("4. Assign Grade to an Enrollment"))
        print(subheading("5. Logout"))

        info("Enter choice: ")
        choice = input().strip()

        # ---------------- Profile ----------------
        if choice == "1":
            heading("\n=== My Profile ===")
            info(str(teacher))

        # ---------------- View Courses ----------------
        elif choice == "2":
            courses = course_service.get_all_courses()
            my_courses = [c for c in courses if getattr(c, 'teacher_id', None) == teacher.teacher_id]
            list_courses(my_courses)

        # ---------------- View Enrollments ----------------
        elif choice == "3":
            courses = course_service.get_all_courses()
            my_courses_ids = {c.course_id for c in courses if getattr(c, 'teacher_id', None) == teacher.teacher_id}
            enrollments = enrollment_service.get_all_enrollments()
            my_enrolls = [e for e in enrollments if e.course_id in my_courses_ids]
            courses_map = {c.course_id: c.name for c in courses}
            list_enrollments(my_enrolls, courses_map)

        # ---------------- Assign Grade ----------------
        elif choice == "4":
            # Ask for student identifier
            student_identifier = input(subheading("Enter Student ID or Email to assign grade (or press Enter to cancel): ")).strip()
            if not student_identifier:
                print(info("Grade assignment cancelled."))
                continue

            # Optionally, select a course (if your enrollment system has multiple courses)
            course_id = input(subheading("Enter Course ID (or press Enter to assign for default/current course): ")).strip() or None

            # Ask for grade
            grade = input(subheading("Enter Grade (e.g., A, B+, C) (or press Enter to cancel): ")).strip().upper()
            if not grade:
                print(info("No grade entered. Cancelled."))
                continue

            # Assign grade using enrollment service
            success_flag = enrollment_service.assign_grade(student_identifier, grade, course_id)
            if success_flag:
                print(success(f"Grade '{grade}' assigned successfully to student '{student_identifier}'" + (f" for course {course_id}" if course_id else "") + "."))
            else:
                print(error("Failed to assign grade. Check Student ID/Email or Course ID."))


        # ---------------- Logout ----------------
        elif choice == "5":
            info("Logging out...")
            break

        else:
            error("Invalid choice. Please select a valid option.")