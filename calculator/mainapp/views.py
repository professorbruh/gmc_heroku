from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from .models import *
from itertools import combinations
from datetime import *

grades_points = {'A': 10, 'B': 8, 'C': 6, 'F': 0}


def login_view(request):
    if request.method == 'POST':
        current_time = datetime.now()
        entry = Lock.objects.all()
        for e in entry:
            timestamp = e.timestamp

            if timestamp.day == current_time.day:
                if timestamp.hour == current_time.hour:
                    if current_time.minute - timestamp.minute <= 5:
                        continue
            e.delete()

        obj = Lock()
        obj.username = request.POST.get('username')
        obj.timestamp = datetime.now()
        obj.save()

        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('type')

        entry = Lock.objects.filter(username=username)
        count = 0
        for e in entry:
            count += 1

        if count >= 5:
            messages.info(request, 'You have typed incorrect username/password too many time. Try after few minutes!')
        else:
            flag = 0
            if user_type == 'student':
                users = Student.objects.all()
                for e in users:
                    if e.username == username:
                        name = e.first_name + e.last_name
                        flag = 1
                        break
            elif user_type == 'advisor':
                users = Advisor.objects.all()
                for e in users:
                    if e.username == username:
                        name = e.first_name + e.last_name
                        flag = 1
                        break
            elif user_type == 'faculty':
                users = Faculty.objects.all()
                for e in users:
                    if e.username == username:
                        flag = 1
                        break

            else:
                users = Coe.objects.all()
                for e in users:
                    if e.username == username:
                        flag = 1
                        break

            user = authenticate(request, username=username, password=password)

            if user is not None and flag == 1:
                entry = Lock.objects.filter(username=username)
                for e in entry:
                    e.delete()
                login(request, user)
                if user_type == 'student':
                    return redirect(view_profile_student_view)
                elif user_type == 'advisor':
                    return redirect(view_profile_advisor_view)
                elif user_type == 'faculty':
                    return redirect(view_profile_faculty_view)
                else:
                    return redirect(view_profile_coe_view)
            else:
                messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect(login_view)


def check_view(request):
    return render(request, 'check.html')


def view_profile_advisor_view(request):
    username = request.user.username
    entry = Advisor.objects.get(username=username)
    first_name = entry.first_name
    last_name = entry.last_name
    year = entry.year

    context = {'username': username, 'first_name': first_name, 'last_name': last_name, 'year': year}

    return render(request, 'Advisor/view_profile.html', context)


def class_details_view(request):
    username = request.user.username
    entry1 = Advisor.objects.get(username=username)
    year = entry1.year

    entry2 = Student.objects.filter(year=year)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Advisor/class_details.html', context)


def view_course_advisor_view(request):
    username = request.user.username
    entry1 = Advisor.objects.get(username=username)
    entry2 = Course.objects.all()
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Advisor/view_course.html', context)


def view_grade_advisor_view(request, course_title):
    username = request.user.username
    entry1 = Advisor.objects.get(username=username)
    entry2 = Grade.objects.get(course_title=course_title)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Advisor/view_grade.html', context)


def view_marks_advisor_view(request):
    username = request.user.username
    entry1 = Advisor.objects.get(username=username)
    entry2 = Course.objects.filter(year=entry1.year)
    entry3 = Student.objects.filter(year=entry1.year)

    roll = {}
    for i in entry3:
        roll[i.username] = i.roll_number
    print(roll)

    course_mark = {}
    for i in entry2:
        course_mark[i.course_title] = {}
        entry4 = Mark.objects.filter(course_title=i.course_title)
        for j in entry4:
            course_mark[i.course_title][j.username_id] = j.marks

    print(course_mark)

    context = {'e1': entry1, 'e2': entry2, 'e3': entry3, 'roll': roll, 'mark': course_mark}
    return render(request, 'Advisor/view_marks.html', context)


def approve_events_view(request):
    if request.method == 'POST':
        entry = Student.objects.all()
        for i in entry:
            if request.POST.get(i.username + "+name"):
                events = request.POST.get(i.username + "+event")
                print(i.username, events)
                row_entry = Event.objects.get(username=i.username)
                row_entry.is_approved = True
                row_entry.save(update_fields=['is_approved'])

                row_entry2 = Student.objects.get(username=i.username)
                grace_marks = min(20, 5 * int(events))
                print(grace_marks)
                row_entry2.grace_marks = grace_marks
                row_entry2.save(update_fields=['grace_marks'])

        messages.success(request, 'Approved!')

    username = request.user.username
    entry1 = Advisor.objects.get(username=username)
    entry2 = Student.objects.filter(year=entry1.year)
    entry3 = Event.objects.filter(is_approved=False)
    context = {'e1': entry1, 'e2': entry2, 'e3': entry3}
    return render(request, 'Advisor/approve_events.html', context)


def view_profile_student_view(request):
    username = request.user.username
    entry1 = Student.objects.get(username=username)
    context = {'e1': entry1}
    return render(request, 'Student/view_profile_student.html', context)


def view_marks_view(request):
    username = request.user.username
    entry1 = Student.objects.get(username=username)
    year = entry1.year

    entry2 = Mark.objects.filter(username=username)

    for i in entry2:
        print(i.course_title_id, i.marks)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Student/view_marks.html', context)


def student_view_course_view(request):
    username = request.user.username
    entry1 = Student.objects.get(username=username)
    entry2 = Course.objects.filter(year=entry1.year)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Student/view_course_grade.html', context)


def student_view_grade_view(request, course_title):
    username = request.user.username
    entry1 = Student.objects.get(username=username)
    entry2 = Grade.objects.get(course_title=course_title)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Student/view_grade.html', context)


def events_form_view(request):
    username = request.user.username

    entry1 = Student.objects.get(username=username)
    eventobj = Event.objects.get(username=username)
    print(eventobj.no_of_events)
    temp = ""
    if request.method == "POST":
        temp = request.POST.get("events")
        eventobj.no_of_events = temp
        eventobj.save(update_fields = ['no_of_events'])

    context = {'e1': entry1, 'e2': eventobj}
    return render(request, 'Student/events_form.html', context)


def view_profile_faculty_view(request):
    username = request.user.username
    entry1 = Faculty.objects.get(username=username)
    context = {'e1': entry1}
    return render(request, 'Faculty/view_profile_faculty.html', context)


def view_course_faculty_view(request):
    username = request.user.username
    entry1 = Faculty.objects.get(username=username)
    entry2 = FacultyCourse.objects.filter(username=username)
    for i in entry2:
        print(i.course_title_id)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Faculty/view_course.html', context)


def view_course_update_faculty_view(request):
    username = request.user.username
    entry1 = Faculty.objects.get(username=username)
    entry2 = FacultyCourse.objects.filter(username=username)
    for i in entry2:
        print(i.course_title_id)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Faculty/view_course_update.html', context)


def view_marks_faculty_view(request, course_title):
    username = request.user.username
    entry1 = Faculty.objects.get(username=username)
    entry_year = Course.objects.get(course_title=course_title)
    year = entry_year.year
    entry2 = Course.objects.filter(year=year)
    entry3 = Student.objects.filter(year=year)

    course_mark = {}
    for i in entry2:
        course_mark[i.course_title] = {}
        entry4 = Mark.objects.filter(course_title=i.course_title)
        for j in entry4:
            course_mark[i.course_title][j.username_id] = j.marks

    print(course_mark)

    roll = {}
    name = {}
    for i in entry3:
        roll[i.username] = i.roll_number
        name[i.username] = i.first_name

    context = {'e1': entry1, 'e2': entry2, 'e3': entry3, 'course_title': course_title, 'mark': course_mark, 'name': name, 'roll': roll}
    return render(request, 'Faculty/view_marks.html', context)


def update_marks_view(request, course_title):
    if request.method == 'POST':
        entry_year = Course.objects.get(course_title=course_title)
        year = entry_year.year
        entry = Student.objects.filter(year=year)
        d = {}
        for i in entry:
            d[i.username] = request.POST.get(i.username)
        print(d)
        for i in d:
            row_entry = Mark.objects.get(username=i, course_title=course_title)
            row_entry.marks = d[i]
            row_entry.save(update_fields=['marks'])
        messages.success(request, 'Form Submitted successfully!')

    username = request.user.username
    entry1 = Faculty.objects.get(username=username)
    entry_year = Course.objects.get(course_title=course_title)
    year = entry_year.year
    entry2 = Course.objects.filter(year=year)
    entry3 = Student.objects.filter(year=year)

    course_mark = {}
    for i in entry2:
        course_mark[i.course_title] = {}
        entry4 = Mark.objects.filter(course_title=i.course_title)
        for j in entry4:
            course_mark[i.course_title][j.username_id] = j.marks

    roll = {}
    name = {}
    for i in entry3:
        roll[i.username] = i.roll_number
        name[i.username] = i.first_name

    context = {'e1': entry1, 'e2': entry2, 'e3': entry3, 'course_title': course_title, 'mark': course_mark,
               'name': name, 'roll': roll}
    return render(request, 'Faculty/update_marks.html', context)


def view_course_grade_view(request):
    username = request.user.username
    entry1 = Faculty.objects.get(username=username)
    entry2 = Course.objects.all()
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Faculty/view_course_grade.html', context)


def view_grade_faculty_view(request, course_title):
    username = request.user.username
    entry1 = Faculty.objects.get(username=username)
    entry2 = Grade.objects.get(course_title=course_title)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'Faculty/view_grade.html', context)


def view_profile_coe_view(request):
    username = request.user.username
    entry1 = Coe.objects.get(username=username)

    context = {'e1': entry1}
    return render(request, 'COE/view_profile_coe.html', context)


def view_course_coe_view(request):
    username = request.user.username
    entry1 = Coe.objects.get(username=username)

    entry2 = Course.objects.all()
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'COE/view_course.html', context)


def update_grade_view(request, course_title):
    if request.method == 'POST':
        entry = Grade.objects.filter(course_title=course_title)
        fromA = request.POST.get('fromA')
        toA = request.POST.get('toA')
        fromB = request.POST.get('fromB')
        toB = request.POST.get('toB')
        fromC = request.POST.get('fromC')
        toC = request.POST.get('toC')
        fromF = request.POST.get('fromF')
        toF = request.POST.get('toF')
        credit = request.POST.get('credit')
        print(fromA, toA, fromB, toB, fromC, toC, fromF, toF, credit)

        row_entry = Grade.objects.get(course_title=course_title)
        row_entry.fromA = fromA
        row_entry.fromB = fromB
        row_entry.fromC = fromC
        row_entry.fromF = fromF
        row_entry.toA = toA
        row_entry.toB = toB
        row_entry.toC = toC
        row_entry.toF = toF
        row_entry.credits = credit

        row_entry.save(update_fields=['fromA', 'fromB', 'fromC', 'fromF', 'toA', 'toB', 'toC', 'toF', 'credits'])
        messages.success(request, 'Form Submitted successfully!')

    username = request.user.username
    entry1 = Coe.objects.get(username=username)

    entry2 = Grade.objects.get(course_title=course_title)
    context = {'e1': entry1, 'e2': entry2}
    return render(request, 'COE/modify_grade.html', context)


def view_year_view(request):
    username = request.user.username
    entry1 = Coe.objects.get(username=username)

    context = {'e1': entry1}
    return render(request, 'COE/view_year.html', context)


def grace_mark_calculate_view(request, year):
    if request.method == 'POST':
        username = request.user.username
        coe_entry = Coe.objects.get(username=username)

        coe_entry.grace_mark_applied = True
        coe_entry.save(update_fields=['grace_mark_applied'])

        student_entry = Student.objects.filter(year=year)
        course_entry = Course.objects.filter(year=year)

        username_course_marks = {}
        username_grace_marks = {}

        for student in student_entry:
            username_grace_marks[student.username] = student.grace_marks
            username_course_marks[student.username] = {}

            mark_entry = Mark.objects.filter(username=student.username)
            for subject in mark_entry:
                course_title = subject.course_title_id
                marks = subject.marks
                username_course_marks[student.username][course_title] = marks

        course_credit = {}
        course_range_marks = {}
        course_list = []

        for course in course_entry:
            course_range_marks[course.course_title] = {}
            course_list.append(course.course_title)
            grade_entry = Grade.objects.get(course_title=course.course_title)
            course_range_marks[course.course_title]['fromA'] = grade_entry.fromA
            course_range_marks[course.course_title]['fromB'] = grade_entry.fromB
            course_range_marks[course.course_title]['fromC'] = grade_entry.fromC
            course_range_marks[course.course_title]['fromF'] = grade_entry.fromF
            course_range_marks[course.course_title]['toA'] = grade_entry.toA
            course_range_marks[course.course_title]['toB'] = grade_entry.toA
            course_range_marks[course.course_title]['toC'] = grade_entry.toA
            course_range_marks[course.course_title]['toF'] = grade_entry.toA
            course_credit[course.course_title] = grade_entry.credits

        username_course_gpa = {}

        for student in username_course_marks:
            username_course_gpa[student] = {}
            for subject in username_course_marks[student]:
                marks = username_course_marks[student][subject]
                course = subject

                if course_range_marks[course]['fromA'] <= marks <= course_range_marks[course]['toA']:
                    username_course_gpa[student][course] = 10 * int(course_credit[course])
                elif course_range_marks[course]['fromB'] <= marks <= course_range_marks[course]['toB']:
                    username_course_gpa[student][course] = 8 * int(course_credit[course])
                elif course_range_marks[course]['fromC'] <= marks <= course_range_marks[course]['toC']:
                    username_course_gpa[student][course] = 6 * int(course_credit[course])
                else:
                    username_course_gpa[student][course] = 0

        total_credits = 0
        for course in course_credit:
            total_credits += int(course_credit[course])
        username_cgpa = {}

        for student in username_course_gpa:
            total_gpa = 0
            for subject in username_course_gpa[student]:
                total_gpa += int(username_course_gpa[student][subject])
            username_cgpa[student] = total_gpa / total_credits

        course_combinations = list(combinations(course_list, 3))
        print(username_course_marks)
        print(username_cgpa)

        for student in student_entry:
            best_marks = {}
            best_marks[student.username] = {}
            username = student.username
            for combination in course_combinations:
                temp_course_marks = {}
                for it in username_course_marks[username]:
                    temp_course_marks[it] = username_course_marks[username][it]

                temp_course_gpa = {}
                for it in username_course_gpa[username]:
                    temp_course_gpa[it] = username_course_gpa[username][it]

                temp_grace_marks = username_grace_marks[username]

                subject_order_list = []
                for subject in combination:
                    marks = username_course_marks[username][subject]
                    if course_range_marks[subject]['fromA'] <= marks <= course_range_marks[subject]['toA']:
                        continue
                    elif course_range_marks[subject]['fromB'] <= marks <= course_range_marks[subject]['toB']:
                        needed = course_range_marks[subject]['fromA'] - marks
                        subject_order_list.append((1, needed, subject))
                    elif course_range_marks[subject]['fromC'] <= marks <= course_range_marks[subject]['toC']:
                        needed = course_range_marks[subject]['fromB'] - marks
                        subject_order_list.append((1, needed, subject))
                    else:
                        needed = course_range_marks[subject]['fromC'] - marks
                        subject_order_list.append((0, needed, subject))

                subject_order_list.sort()
                if len(subject_order_list) == 0:
                    continue
                else:
                    for it in subject_order_list:
                        needed = it[1]
                        subject = it[2]
                        if temp_grace_marks >= needed:
                            temp_grace_marks -= needed
                            temp_course_marks[subject] += needed
                        else:
                            continue

                for course in temp_course_marks:
                    marks = temp_course_marks[course]
                    if course_range_marks[course]['fromA'] <= marks <= course_range_marks[course]['toA']:
                        temp_course_gpa[course] = 10 * int(course_credit[course])
                    elif course_range_marks[course]['fromB'] <= marks <= course_range_marks[course]['toB']:
                        temp_course_gpa[course] = 8 * int(course_credit[course])
                    elif course_range_marks[course]['fromC'] <= marks <= course_range_marks[course]['toC']:
                        temp_course_gpa[course] = 6 * int(course_credit[course])
                    else:
                        temp_course_gpa[course] = 0

                temp_cgpa = 0
                for gpa in temp_course_gpa:
                    temp_cgpa += temp_course_gpa[gpa]
                temp_cgpa = temp_cgpa / total_credits
                if username_cgpa[username] < temp_cgpa:
                    username_cgpa[username] = temp_cgpa
                    best_marks[username] = temp_course_marks
            count = 0
            for it in best_marks[username]:
                count += 1
            if count > 0:
                username_course_marks[username] = best_marks[username]
        print(username_course_marks)
        print(username_cgpa)

        for student in student_entry:
            student_row_entry = Student.objects.get(username=student.username)
            student_row_entry.grace_marks = 0
            student_row_entry.cgpa = username_cgpa[student.username]
            student_row_entry.save(update_fields=['grace_marks', 'cgpa'])
            mark_entry = Mark.objects.filter(username=student.username)
            for subject in mark_entry:
                title = subject.course_title_id
                marks = username_course_marks[student.username][title]
                subject.marks = marks
                subject.save(update_fields=['marks'])

    username = request.user.username
    entry1 = Coe.objects.get(username=username)
    entry2 = Course.objects.filter(year=year)
    entry3 = Student.objects.filter(year=year)

    roll = {}
    grace = {}
    credit = {}
    for i in entry3:
        roll[i.username] = i.roll_number
        grace[i.username] = i.grace_marks

    course_mark = {}
    for i in entry2:
        course_mark[i.course_title] = {}
        credit[i.course_title] = Grade.objects.get(course_title=i.course_title).credits
        entry4 = Mark.objects.filter(course_title=i.course_title)
        for j in entry4:
            course_mark[i.course_title][j.username_id] = j.marks

    context = {'e1': entry1, 'e2': entry2, 'e3': entry3, 'roll': roll, 'mark': course_mark, 'grace': grace, 'credit': credit}
    return render(request, 'COE/grace_mark_calculate.html', context)


def advisor_change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():

            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('view_profile_advisor')
        else:
            messages.error(request, "Please Correct the error")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Advisor/change_password.html', {'form': form})


def student_change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('view_profile_student')
        else:
            messages.error(request, "Please Correct the error")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Student/change_password.html', {'form': form})


def faculty_change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('view_profile_faculty')
        else:
            messages.error(request, "Please Correct the error")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Faculty/change_password.html', {'form': form})


def coe_change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('view_profile_coe')
        else:
            messages.error(request, "Please Correct the error")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'COE/change_password.html', {'form':form})


def events_form(request):
    username = request.user.username

    entry1 = Student.objects.get(username = username)
    eventobj = Event.objects.get(username=username)
    print(eventobj.no_of_events)
    temp = ""
    if request.method == "POST":
        temp = request.POST.get("events")
        eventobj.no_of_events = temp
        eventobj.save(update_fields = ['no_of_events'])

    context = {'e1': entry1, 'e2': eventobj}
    return render(request, 'Student/Events_form.html', context)

