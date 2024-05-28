from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .forms import RegistrationForm, StudentProfileForm, FacultyProfileForm, EmployeeProfileForm, ComplaintForm, ReviewForm, ChangeReviewerForm
from .models import User, Student, Faculty, Employee, Complaint
# from .serializer import ComplaintSerializer, StudentSerializer, UserSerializer, FacultySerializer, EmployeeSerializer, ComplaintSerializer
# from rest_framework.generics import ListAPIView

# Create your views here.
class UserView(View):
    def get(self, request):
        return render(request, 'newapp/home.html')

#Lodge Complaints
class LodgeView(View):
    def get(self,request):
        form = ComplaintForm()
        return render(request, 'newapp/lodge.html' , {'form':form})
    def post(self, request):
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            usr = request.user
            complainer = form.cleaned_data['complainer']
            accused = form.cleaned_data['accused']
            accused_status = form.cleaned_data['accused_status']
            reviewer = request.POST.get('reviewer')
            statement = form.cleaned_data['statement']
            upload = form.cleaned_data['upload']
            reg = Complaint(user=usr, complainer=complainer, accused=accused,accused_status=accused_status,
            reviewer=reviewer, statement=statement, upload=upload)
            reg.save()
            messages.success(request, 'Congratulations!! Complaint Lodged Successfully')
        return render(request, 'newapp/lodge.html' , {'form':form})

# Review By Reviewer
class DetailedReviewView(View):
    def get(self, request, pk):
        form = ReviewForm()
        complaints = Complaint.objects.get(pk=pk)
        return render(request,'newapp/detailedreview.html', {'complaints':complaints, 'form':form})
    def post(self, request, pk):
        # form = ComplaintForm(request.POST)
        complaints = Complaint.objects.get(pk=pk)
        # reviewer = request.POST.get('reviewer')
        status = request.POST.get('status')
        comment = request.POST.get('comment')
        complaints.status = status
        complaints.comment = comment
        # complaints.reviewer = reviewer
        complaints.save()
        messages.success(request, 'Congratulations!! Complaint Reviewed Successfully')
        return render(request, 'newapp/reviewdone.html')

# Change Reviewer and shift to another reviewer
class ChangeReviewerView(View):
    def get(self, request, pk):
        form = ChangeReviewerForm()
        complaints = Complaint.objects.get(pk=pk)
        return render(request,'newapp/changereviewer.html', {'complaints':complaints, 'form':form})
    def post(self, request, pk):
        # form = ChangeReviewerForm(request.POST)
        complaints = Complaint.objects.get(pk=pk)
        reviewer = request.POST.get('reviewer')
        status = request.POST.get('status')
        comment = request.POST.get('comment')
        complaints.status = status
        complaints.comment = comment
        complaints.reviewer = reviewer
        complaints.save()
        messages.success(request, 'Congratulations!! Complaint Reviewed Successfully')
        return render(request, 'newapp/reviewdone.html')

# View after Login
class ProfileView(View):
    def get(self,request):
        return render(request, 'newapp/profile.html')

# Informations about logged in user
def information(request):
    usr = request.user
    if usr.position == 'Student':
        try:
            stud = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            stud = None

        return render(request, 'newapp/info.html',{'info':usr,'stud':stud, 'active':'btn-primary'})
    elif usr.position == 'Faculty':
        if usr.is_staff:
            return render(request, 'newapp/info.html',{'info':usr, 'active':'btn-primary'})
        else:
            try:
                fac = Faculty.objects.get(user=request.user)
            except Faculty.DoesNotExist:
                fac = None

            return render(request, 'newapp/info.html',{'info':usr,'fac':fac, 'active':'btn-primary'})
    elif usr.position == 'Employee':
        try:
            emp = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            emp = None

        return render(request, 'newapp/info.html',{'info':usr,'emp':emp, 'active':'btn-primary'})
    else:
        return render(request, 'newapp/info.html',{'info':usr, 'active':'btn-primary'})

# Shows available complaints to reviewer
def ReviewsView(request):
    usr = request.user
    try:
        comp = Complaint.objects.filter(reviewer=usr)
    except Complaint.DoesNotExist:
        comp = None
    return render(request, 'newapp/review.html',{'comp':comp, 'active':'btn-primary'})

# Shows lodged comolaints to the complainer
def ComplaintsView(request):
    add = Complaint.objects.filter(user=request.user)
    return render(request, 'newapp/complaints.html',{'add':add, 'active':'btn-primary'})

# Shows prodfile informations of logged in user according to their positions and change informations
class UserProfileView(View):
    def get(self,request):
        usr = request.user
        if usr.position == 'Student':
            form = StudentProfileForm()
            return render(request, 'newapp/userprofile.html' , {'form':form, 'active':'btn-primary'})
        elif usr.position == 'Faculty':           
            form = FacultyProfileForm()
            return render(request, 'newapp/userprofile.html' , {'form':form, 'active':'btn-primary'})
        elif usr.position == 'Employee':           
            form = EmployeeProfileForm()
            return render(request, 'newapp/userprofile.html' , {'form':form, 'active':'btn-primary'})

    def post(self,request):
        usr = request.user
        if usr.position == 'Student':
            form = StudentProfileForm(request.POST)
            if form.is_valid():
                usr = request.user
                name = form.cleaned_data['name']
                student_id = form.cleaned_data['student_id']
                reg = Student(user=usr, name=name, student_id=student_id)
                reg.save()
                messages.success(request, "Congratulations information updated successfully!!")
            return render(request, 'newapp/profile.html', {'form':form, 'active':'btn-primary'})
        elif usr.position == 'Faculty':
            form = FacultyProfileForm(request.POST)
            if form.is_valid():
                usr = request.user
                name = form.cleaned_data['name']
                faculty_initial = form.cleaned_data['faculty_initial']
                reg = Faculty(user=usr, name=name, faculty_initial=faculty_initial)
                reg.save()
                messages.success(request, "Congratulations information updated successfully!!")
            return render(request, 'newapp/profile.html', {'form':form, 'active':'btn-primary'})
        elif usr.position == 'Employee':
            form = EmployeeProfileForm(request.POST)
            if form.is_valid():
                usr = request.user
                name = form.cleaned_data['name']
                employee_id = form.cleaned_data['employee_id']
                sector = form.cleaned_data['sector']
                reg = Employee(user=usr, name=name, employee_id=employee_id, sector=sector)
                reg.save()
                messages.success(request, "Congratulations information updated successfully!!")
            return render(request, 'newapp/profile.html', {'form':form, 'active':'btn-primary'})

# Registration form for new user
class RegistrationView(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request, 'newapp/registration.html' , {'form':form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! Successfully Registered')
        return render(request, 'newapp/registration.html' , {'form':form})

# #API
# class StudentList(ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

# class FacultyList(ListAPIView):
#     queryset = Faculty.objects.all()
#     serializer_class = FacultySerializer

# class EmployeeList(ListAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

# class UserList(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class ComplaintsList(ListAPIView):
#     queryset = Complaint.objects.all()
#     serializer_class = ComplaintSerializer