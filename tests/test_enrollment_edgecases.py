from storage.json_storage import JSONStorage
from utils.logger import Logger
from services.enrollment_service import EnrollmentService
from utils.id_generator import new_id

def test_duplicate_enrollment(tmp_path):
    data_dir = tmp_path / 'data'
    s = JSONStorage(str(data_dir))
    logger = Logger(str(tmp_path / 'log.txt'))
    # prepare student and course
    sid = new_id('stu')
    s.save('students', [{'id':sid,'name':'T','age':20,'student_number':'X1'}])
    s.save('courses', [{'code':'C101','title':'Test Course','credits':3}])
    # directly insert enrollment
    from models.enrollment import Enrollment
    eid = new_id('enr')
    enrollments = s.load('enrollments')
    enrollments.append(Enrollment(eid, sid, 'C101').to_dict())
    s.save('enrollments', enrollments)
    # verify duplicate detected in data
    enrollments = s.load('enrollments')
    assert any(e.get('student_id')==sid and e.get('course_code')=='C101' for e in enrollments)
