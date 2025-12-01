from storage.json_storage import JSONStorage
from models.teacher import Teacher

def test_teacher_storage(tmp_path):
    # Setup a file path
    storage_file = tmp_path / "teachers.json"
    storage = JSONStorage(str(storage_file))

    # Add a sample teacher
    from utils.id_generator import generate_id
    teacher = Teacher(generate_id("T"), "Admin Teacher", "admin@gmail.com", "password")
    storage.add(teacher)

    # Reload teachers and assert at least one exists
    teachers = storage.load(Teacher)
    assert len(teachers) > 0
    assert any(t.email == "admin@gmail.com" for t in teachers)
