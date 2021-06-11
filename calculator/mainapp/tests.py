from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.test import TestCase, Client
from .views import *
from .models import *
from .forms import *


class TestUrls(SimpleTestCase):
    def test_home_url(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, login_view)

    def test_logout_url(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout_view)

    def test_advisor_profile_url(self):
        url = reverse('view_profile_advisor')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_profile_advisor_view)

    def test_advisor_class_url(self):
        url = reverse('class_details')
        print(resolve(url))
        self.assertEquals(resolve(url).func, class_details_view)

    def test_advisor_course_url(self):
        url = reverse('view_course_advisor')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_course_advisor_view)

    def test_advisor_marks_url(self):
        url = reverse('view_marks_advisor')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_marks_advisor_view)

    def test_advisor_approve_url(self):
        url = reverse('approve_events')
        print(resolve(url))
        self.assertEquals(resolve(url).func, approve_events_view)

    def test_student_profile_url(self):
        url = reverse('view_profile_student')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_profile_student_view)

    def test_student_marks_url(self):
        url = reverse('view_marks')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_marks_view)

    def test_student_course_url(self):
        url = reverse('student_view_course')
        print(resolve(url))
        self.assertEquals(resolve(url).func, student_view_course_view)

    def test_student_events_url(self):
        url = reverse('events')
        print(resolve(url))
        self.assertEquals(resolve(url).func, events_form_view)

    def test_faculty_profile_url(self):
        url = reverse('view_profile_faculty')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_profile_faculty_view)

    def test_faculty_course_url(self):
        url = reverse('view_course_faculty')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_course_faculty_view)

    def test_faculty_update_course_url(self):
        url = reverse('view_course_update_faculty')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_course_update_faculty_view)

    def test_faculty_view_grade_url(self):
        url = reverse('view_course_grade')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_course_grade_view)

    def test_coe_profile_url(self):
        url = reverse('view_profile_coe')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_profile_coe_view)

    def test_coe_view_course_url(self):
        url = reverse('view_course_coe')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_course_coe_view)

    def test_coe_view_level_url(self):
        url = reverse('view_level')
        print(resolve(url))
        self.assertEquals(resolve(url).func, view_year_view)


class ViewTest(TestCase):
    def test_logout_view(self):
        client = Client()
        response = client.get(reverse('logout'))
        return self.assertEquals(response.status_code, 302)


class AdvisorTest(TestCase):
    def create_advisor(self, username="Hugh123", first_name="Hugh", last_name="Nichols", year=1):
        return Advisor.objects.create(username=username, first_name=first_name, last_name=last_name, year=year)

    def create_wrong_advisor_1(self, username="Hugh123", first_name="Hugh", last_name="Nichols", year="Tap"):
        return Advisor.objects.create(username=username, first_name=first_name, last_name=last_name, year=year)

    def test_advisor_create(self):
        w = self.create_advisor()
        self.assertTrue(isinstance(w, Advisor))

    # def test_advisor_create2(self):
    #    w = self.create_wrong_advisor_1()
    #    self.assertFalse(isinstance(w, Advisor))


class StudentTest(TestCase):
    def create_Student(self, username="Leslie123", roll_number="R102", first_name="Leslie", last_name="Goodman",
                       year=1):
        return Student.objects.create(username=username, roll_number=roll_number, first_name=first_name,
                                      last_name=last_name, year=year)

    def test_Student_create(self):
        w = self.create_Student()
        self.assertTrue(isinstance(w, Student))


class FacultyTest(TestCase):
    def create_Faculty(self, username="Nolan123", first_name="Nolan", last_name="Harding"):
        return Faculty.objects.create(username=username, first_name=first_name, last_name=last_name)

    def test_Faculty_create(self):
        w = self.create_Faculty()
        self.assertTrue(isinstance(w, Faculty))


class CourseTest(TestCase):
    def create_Course(self, course_title="CSE102", year=1):
        return Course.objects.create(course_title=course_title, year=year)

    def test_Course_create(self):
        w = self.create_Course()
        self.assertTrue(isinstance(w, Course))


class CoeTest(TestCase):
    def create_Coe(self, username="Pranav123", first_name="Pranav", last_name="Stephens"):
        return Coe.objects.create(username=username, first_name=first_name, last_name=last_name)

    def test_Coe_create(self):
        w = self.create_Coe()
        self.assertTrue(isinstance(w, Coe))


class FormUpdateMarksTest(SimpleTestCase):
    def test_update_marks_form_valid(self):
        form = UpdateMarksForm(data={
            'roll_number': 'CSE101',
            'name': 'Ram',
            'marks': 100
        })

        self.assertTrue(form.is_valid())

    def test_update_marks_form_no_data(self):
        form = UpdateMarksForm(data={
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_update_marks_invalid(self):
        form = UpdateMarksForm(data={
            'roll_number': 'CSE101',
            'name': 'Ram'
        })
        self.assertEquals(len(form.errors), 1)


class FormEventTest(SimpleTestCase):
    def test_events_valid(self):
        form = EventsForm(data={
            'no_of_events': 5,
        })

        self.assertTrue(form.is_valid())

    def test_events_invalid(self):
        form = EventsForm(data={
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class FormModifyGradeTest(SimpleTestCase):
    def test_modify_grade_valid(self):
        form = ModifyGradeForm(data={
            'fromA': 85,
            'toA': 100,
            'fromB': 60,
            'toB': 84,
            'fromC': 45,
            'toC': 59,
            'fromF': 0,
            'toF': 44,
            'credits': 3,
        })
        self.assertTrue(form.is_valid())

    def test_modify_grade_invalid(self):
        form = ModifyGradeForm(data={
            'fromA': 85,
            'toA': 100,
            'fromB': 60,
            'toB': 84,
            'fromC': 45,
            'toC': 59,
            'fromF': 0,
            'toF': 44
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class FormChangePasswordTest(SimpleTestCase):
    def test_change_password_valid(self):
        form = ChangePasswordForm(data={
            'old_password': 'abcd',
            'new_password': 'abcd1',
            'confirm_new_password': 'abcd1'
        })

        self.assertTrue(form.is_valid())
