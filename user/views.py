from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .models import CustomUser
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView


def register_page(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.set_password(user.password)
            user.is_active = False
            user.save()

            # creates 6 digit code:

            user.generate_verification_code()

            subject = "Email Verification Code"
            message = render_to_string(
                'user/verify_email_message.html',
                {
                    'user': user,
                    'code': user.email_verification_code
                }
            )

            email = EmailMessage(
                subject,
                message,
                to=[user.email]
            )
            email.content_subtype = 'html'
            email.send()

            return redirect('user:verify-code')

    return render(request, 'user/register.html', {'form': form})


def verify_email_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        try:
            user = CustomUser.objects.get(
                email_verification_code=code,
                is_active=False
            )
        except CustomUser.DoesNotExist:
            messages.error(request, 'Wrong code or code has been expired')
            return redirect('user:verify-code')

        user.is_active = True
        user.email_verification_code = None
        user.save()

        login(request,user)
        return redirect('upskill:index')

    return render(request, 'user/verify_code.html')


# def verify_email_confirm(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = CustomUser.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Your email has been verified.')
#         return HttpResponse('Successfully verified!')
#     else:
#         messages.warning(request, 'The link is invalid.')
#         return HttpResponse('OOPS! Something is wrong')


