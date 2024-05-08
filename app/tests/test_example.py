import pytest

def test_equal_to(): 
    assert 3 == 3

def test_list():
    num_list = [1, 2, 3]
    any_list = [False, False]
    assert 3 in num_list
    assert 6 not in num_list
    assert all(num_list)
    assert not any(any_list)


class Student:
    def __init__(
            self, 
            first_name: str, 
            last_name: str, 
            major: str, 
            years: int
        ):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student('John', 'Doe', 'Computer Science', 3)


def test_person(default_student):
    assert default_student.first_name == 'John'
    assert default_student.last_name == 'Doe'
    assert default_student.major == 'Computer Science'

    
