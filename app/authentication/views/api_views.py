from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from rest_framework import viewsets
from rest_framework import permissions

from app.authentication.forms import LoginForm, SignUpForm, ProfileForm
from app.authentication.serializers import GroupSerializer, UserSerializer, PermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', ]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', ]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', ]


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    context = {'segment': 'home'}
                    html_template = loader.get_template('index.html')
                    return HttpResponse(html_template.render(context, request))
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def profile_user(request):
    success = False
    form = ProfileForm(request.POST or {'id': request.user.id, 'username': request.user.username, "firstname": request.user.first_name,
                                        "lastname": request.user.last_name, "email": request.user.email})
    if not form.is_bound:
        form = ProfileForm()

    if request.method == "POST":

        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(username=request.user)
                user.email = email
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                messages.success(request, 'Saved successfully!')
                success = True
            except User.DoesNotExist:
                messages.success(request, 'User Doesnt found')

    return render(request, "page-user.html", {"form": form, "success": success})
