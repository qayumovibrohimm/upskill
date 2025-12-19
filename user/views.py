from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages


from .tokens import account_activation_token

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # User yaratish
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.is_active = False
        user.save()

        # Activation email
        current_site = get_current_site(request)
        mail_subject = 'Hisobingizni aktivlashtiring'
        message = render_to_string('user/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        email_msg = EmailMessage(mail_subject, message, to=[user.email])
        email_msg.send()

        messages.success(request, 'Emailingizga activation link yuborildi')
        return redirect('login')

    return render(request, 'user/register.html')



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # Avtomatik login
        return redirect('home')
    else:
        return render(request, 'user/activation_invalid.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')  # email ishlatayapmiz
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.username}!")
                return redirect('home')  # home page yoki dashboard
            else:
                messages.error(request, "Hisobingiz aktivlashtirilmagan. Emailni tekshiring.")
        else:
            messages.error(request, "Username yoki parol noto‘g‘ri.")
    return render(request, 'user/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Siz muvaffaqiyatli logout qilindingiz.")
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')
