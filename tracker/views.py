from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from datetime import date, timedelta
import json

from .models import Marks, Assignment, Task

# ---------------- Home ----------------
def home(request):
    return render(request,'index.html')

# ---------------- Register ----------------
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request,"Registration Successful! Please Login.")
            return redirect('login')
        else:
            messages.error(request,"Passwords do not match")
    return render(request,'register.html')

# ---------------- Login ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid username or password")
    return render(request,'login.html')

# ---------------- Dashboard ----------------
@login_required
def dashboard(request):
    # Marks data for chart
    marks = Marks.objects.filter(user=request.user)
    subjects, percentages = [], []
    total_percentage = 0

    for m in marks:
        percent = (m.marks_obtained / m.total_marks) * 100
        subjects.append(m.subject)
        percentages.append(round(percent,1))
        total_percentage += percent

    avg_marks = round(total_percentage / len(percentages),1) if percentages else 0

    # Pending assignments count
    pending_assignments = Assignment.objects.filter(user=request.user, completed=False).count()

    # Upcoming assignments (next 3)
    upcoming = Assignment.objects.filter(user=request.user, completed=False).order_by('due_date')[:3]

    # Task completion %
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, completed=True).count()
    task_percent = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    context = {
        "subjects": json.dumps(subjects),
        "scores": json.dumps(percentages),
        "avg_marks": avg_marks,
        "pending_assignments": pending_assignments,
        "task_percent": task_percent,
        "upcoming": upcoming
    }
    return render(request,"dashboard.html",context)

# ---------------- Logout ----------------
def logout_view(request):
    logout(request)
    return redirect('home')

# ---------------- Marks ----------------
def marks_page(request):
    if request.method == "POST":
        Marks.objects.create(
            user=request.user,
            exam_name=request.POST.get('exam'),
            subject=request.POST.get('subject'),
            marks_obtained=request.POST.get('marks'),
            total_marks=request.POST.get('total'),
            date=request.POST.get('date')
        )
        return redirect('marks')
    data = Marks.objects.filter(user=request.user)
    return render(request,'marks.html',{'data':data})

def delete_mark(request,id):
    Marks.objects.get(id=id).delete()
    return redirect('marks')

def edit_mark(request,id):
    mark = Marks.objects.get(id=id)
    if request.method=="POST":
        mark.exam_name=request.POST.get('exam')
        mark.subject=request.POST.get('subject')
        mark.marks_obtained=request.POST.get('marks')
        mark.total_marks=request.POST.get('total')
        mark.date=request.POST.get('date')
        mark.save()
        return redirect('marks')
    return render(request,'edit_mark.html',{'mark':mark})

# ---------------- Assignments ----------------
from datetime import date, timedelta
from django.core.mail import send_mail

def assignment_page(request):
    if request.method == "POST":
        update_id = request.POST.get('update_id')
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        due = request.POST.get('due_date')

        # convert due date string → date object
        due_date_obj = date.fromisoformat(due)

        if update_id:
            assignment = Assignment.objects.get(id=update_id, user=request.user)
            assignment.name = name
            assignment.subject = subject
            assignment.due_date = due_date_obj
            assignment.save()
        else:
            assignment = Assignment.objects.create(
                user=request.user,
                name=name,
                subject=subject,
                due_date=due_date_obj
            )

            # ------------------------------
            # INSTANT REMINDER WHEN DUE = TOMORROW
            # ------------------------------
            tomorrow = date.today() + timedelta(days=1)
            if assignment.due_date == tomorrow:
                send_mail(
                    "Assignment Reminder",
                    f"""
Hello {assignment.user.username},

Your assignment "{assignment.name}" for subject {assignment.subject} 
is due tomorrow ({assignment.due_date}).

Please complete it before the deadline.

- EduTrackr
                    """,
                    "divyadalbanjan4@gmail.com",
                    [assignment.user.email],
                    fail_silently=False
                )
                print("Instant reminder sent (due date is tomorrow).")

        return redirect('assignment')

    assignments = Assignment.objects.filter(user=request.user).order_by('completed', 'due_date')
    today = date.today()
    soon = today + timedelta(days=2)
    return render(request, 'assignment.html', {'assignments': assignments, 'today': today, 'soon': soon})

def delete_assignment(request, id):
    Assignment.objects.get(id=id, user=request.user).delete()
    return redirect('assignment')

def complete_assignment(request, id):
    assignment = Assignment.objects.get(id=id, user=request.user)
    assignment.completed = not assignment.completed
    assignment.save()
    return redirect('assignment')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task


from datetime import date,timedelta

@login_required
def task_page(request):

    if request.method == "POST":

        # Update task
        if request.POST.get("update_id"):

            task = Task.objects.get(id=request.POST.get("update_id"))

            task.title = request.POST.get("title")
            task.priority = request.POST.get("priority")
            task.due_date = request.POST.get("due_date")

            task.save()

            return redirect("task")

        # Add task
        title = request.POST.get("title")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")

        Task.objects.create(
            user=request.user,
            title=title,
            priority=priority,
            due_date=due_date
        )

        return redirect("task")

    tasks = Task.objects.filter(user=request.user).order_by("completed","due_date")

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    today = date.today()
    soon = today + timedelta(days=2)

    context = {
        "tasks":tasks,
        "total_tasks":total_tasks,
        "completed_tasks":completed_tasks,
        "pending_tasks":pending_tasks,
        "today":today,
        "soon":soon
    }

    return render(request,"task.html",context)

# Toggle complete
@login_required
def complete_task(request,id):

    task = get_object_or_404(Task,id=id,user=request.user)

    task.completed = not task.completed
    task.save()

    return JsonResponse({"status":"success","completed":task.completed})


# Delete task
@login_required
def delete_task(request, id):

    task = get_object_or_404(Task, id=id, user=request.user)

    task.delete()

    return redirect("task")


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


# ---------------- PROFILE ----------------
@login_required
def profile(request):
    return render(request, "profile.html", {
        "user": request.user
    })


# ---------------- EDIT PROFILE ----------------
@login_required
def edit_profile(request):

    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "edit_profile.html")


# ---------------- CHANGE PASSWORD ----------------
@login_required
def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "change_password.html", {"form": form})
