from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import random
import string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from account.models import KycInfo, Account, PostProject, Categories
from rest_framework.views import APIView
from account.api.serializers import RegistrationSerializer, LoginSerializer, KYCInfoSerializer, PostProjectSerializer, \
    CategoriesSerializer, CategorySubCategoryList
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from random import choice
from string import ascii_lowercase, digits, hexdigits, ascii_uppercase
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework.response import Response
from django.core.validators import validate_email

from account.api.forms import PasswordResetRequestForm
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.views.generic import FormView
from django.template import loader
from django.core.mail import send_mail
from django.contrib import messages



@api_view(['POST', ])
def sendHTMLEmail(request):
    subject, from_email, to = 'Confirm your Account', 'testartomatestudio@gmail.com', 'mailme622@gmail.com'
    text_content = 'This is an important message.'
    html_content = '<h1>Greetings!</h1>' \
                   '<h3>Thanks for Registering in our website.</h3>' \
                   '<p>Inorder to confirm your account please click the following link</p>' \
                   '<br><a href="http://www.google.com">http://www.google.com - Activation Link</a>' \
                   '<p>Thankyou!</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return Response('Done')


@api_view(['POST', ])
def registration_view(request):
    user = request.data['username']

    if user == 'yes':
        string2 = ''.join(choice(digits) for i in range(8))
        string3 = ''.join(choice(ascii_lowercase) for i in range(3))
        randomstring = 'f' + string2 + string3
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = False
            account.username = randomstring
            account.is_freelancer = 1
            account.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html',
                                       {
                                           'user': account,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(account.pk)),
                                           'token': account_activation_token.make_token(account),
                                       })
            mail_subject = 'Thank you for registering to our site'
            to_email = request.data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            data['response'] = 'successfully registered new user and ' \
                               'Please confirm your email address to complete the registration '
        else:
            data = serializer.errors
        return Response(data)

    elif user == 'no':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            account.username = ''
            account.is_freelancer = 0
            account.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html',
                                       {
                                           'user': account,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(account.pk)),
                                           'token': account_activation_token.make_token(account),
                                       })
            mail_subject = 'Thank you for registering to our site'
            to_email = request.data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            data['response'] = 'successfully registered new user and ' \
                               'Please confirm your email address to complete the registration '
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST', ])
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        account = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        account = None
    if account is not None and account_activation_token.check_token(account, token):
        account.is_active = True
        account.save()
        return Response('Account Verified')
    else:
        return HttpResponse('Activation link is invalid!')


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_200_OK)
    
    token, _ = Token.objects.get_or_create(user=user)
    postpro = KycInfo.objects.filter(userid=user.id)
    if postpro.exists():
        for kyc in postpro:
            if kyc.kycstatus == 1:
                return Response({'token': token.key, 'kyc_message': 'kyc details uploaded', 'kyc_status': 1},
                                status=HTTP_200_OK)
            elif kyc.kycstatus == 2:
                return Response({'token': token.key, 'kyc_message': 'kyc details pending', 'kyc_status': 2},
                                status=HTTP_200_OK)
            elif kyc.kycstatus == 3:
                return Response({'token': token.key, 'kyc_message': 'kyc details Accepted', 'kyc_status': 3},
                                status=HTTP_200_OK)
            else:
                if kyc.kycstatus == 4:
                    return Response({'token': token.key,'kyc_message': 'kyc details Rejected', 'kyc_status': 4},
                                    status=HTTP_200_OK)
    return Response({'token': token.key, 'kyc_message': 'kyc details not entered', 'kyc_status': 0},
                    status=HTTP_200_OK)


class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {
            "username": request.user.username,
            "email": request.user.email
        }
        return JsonResponse(data)


class KycView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            id = user.id
            postpro = KycInfo.objects.filter(userid=id)
            if postpro.exists():
                for kycstat in postpro:
                    serializer = KYCInfoSerializer(data=request.data)
                    data = {}
                    if kycstat.kycstatus == 1:
                        data['result'] = 'already entered kyc details'
                        data['status'] = 0
            else:
                serializer = KYCInfoSerializer(data=request.data)
                data = {}
                if serializer.is_valid():
                    kyc = serializer.save()
                    kyc.username = user.username
                    kyc.userid = user.id
                    kyc.kycstatus = 1
                    kyc.save()
                    data['result'] = 'success'
                    data['status'] = 1
                else:
                    data['status'] = 0
                    data = serializer.errors
        return Response(data)


class getKYC(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        token, _ = Token.objects.get_or_create(user=request.user)
        postpro = KycInfo.objects.filter(userid=request.user.id)
        if postpro.exists():
            for kyc in postpro:
                if kyc.kycstatus == 2:
                    return Response({'kyc_message':'Pending', 'kyc_status':2}, status=HTTP_200_OK)
                elif kyc.kycstatus == 3:
                    return Response({'kyc_message':'Accepted', 'kyc_status':3}, status=HTTP_200_OK)
                else:
                    if kyc.kycstatus == 4:
                        return Response({'kyc_message':'Rejected', 'kyc_status':4}, status=HTTP_200_OK)
        return Response({'kyc_message': 'kyc not Completed', 'kyc_status': 0}, status=HTTP_200_OK)
        



class AllProjects(APIView):
    def get(self, request):
        queryset = PostProject.objects.all()
        serializer = PostProjectSerializer(queryset, many=True)
        return Response(serializer.data)


class Projects(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            size = 3
            code = 'PR' + ''.join(random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
            user = request.user
            serializer = PostProjectSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                pro = serializer.save()
                pro.userid = user.id
                pro.projectcode = code
                pro.username = user.username
                pro.save()
                data['result'] = 'success'
                data['status'] = 1
            else:
                data['status'] = 0
                data = serializer.errors
            return Response(data)


@api_view(["GET"])
def generate(size):
    size = 3
    code = 'PR' + ''.join(random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
    # if check_if_duplicate(code):
    #     return generate(size=5)
    return Response(code)


class Category(APIView):
    def post(self, request):
        if request.method == 'POST':
            size = 3
            catcode = 'CAT' + ''.join(random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
            subcatcode = 'SUBCAT' + ''.join(
                random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
            serializer = CategoriesSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                category = serializer.save()
                category.categorycode = catcode
                category.subcategorycode = subcatcode
                category.save()
                data['result'] = 'success'
                data['status'] = 1
            else:
                data['status'] = 0
                data = serializer.errors
            return Response(data)


class CategoryList(APIView):
    def post(self, request):
        categoryname = request.data['categoryname']

        print('####################')
        categorkkaka = Categories.objects.filter(categoryname=categoryname).values()
        return JsonResponse({"categories": list(categorkkaka)})

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# class ResetPasswordRequestView(APIView):
#     print(123)
#     template_name = "account/test_template.html"
    
#     success_url = 'api/account/login'
#     form_class = PasswordResetRequestForm
 
#     @api_view(["POST"])
#     def validate_email_address(self,email):
#         try:
#             validate_email(email)
#             return True
#         except ValidationError:
#             return False
#     @api_view(["POST"])
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             data= form.cleaned_data["email_or_username"]
#         # if self.validate_email_address(data) is True:                 #uses the method written above
#             '''
#             If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
#             '''
#             associated_users= Account.objects.filter(Q(email=data)|Q(username=data))
#             current_site = get_current_site(request)
#             if associated_users.exists():
#                 for user in associated_users:
#                         c = {
#                             'email': user.email,
#                             'domain': current_site.domain,
#                             'site_name': 'your site',
#                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                             'user': user,
#                             'token':  account_activation_token.make_token(user),
#                             'protocol': 'http',
#                             }

#                         subject_template_name='registration/password_reset_subject.txt'
#                         # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
#                         email_template_name='account/password_reset_email.html'
#                         # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
#                         subject = loader.render_to_string(subject_template_name, c)
#                         # Email subject *must not* contain newlines
#                         subject = 'password reset'
#                         from_email = 'testartomatestudio@gmail.com'
#                         recipent_list = request.data['email']
#                         message = render_to_string(email_template_name, c)
#                         send_mail(subject,message, from_email, recipent_list)
#                 result = self.form_valid(form) 
#                 messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
#                 return result
#             result = self.form_invalid(form)
#             messages.error(request, 'No user is associated with this email address')
#             return result
#         # else:
#         #     '''
#         #     If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
#         #     '''
#         #     associated_users= User.objects.filter(username=data)
#         #     if associated_users.exists():
#         #         for user in associated_users:
#         #             c = {
#         #                     'email': user.email,
#         #                     'domain': current_site.domain,
#         #                     'site_name': 'your site',
#         #                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         #                     'user': user,
#         #                     'token':  account_activation_token.make_token(user),
#         #                     'protocol': 'http',
#         #                     }
#         #             subject_template_name='registration/password_reset_subject.txt'
#         #             email_template_name='registration/password_reset_email.html'
#         #             subject = loader.render_to_string(subject_template_name, c)
#         #             # Email subject *must not* contain newlines
#         #             subject = ''.join(subject.splitlines())
#         #             email = loader.render_to_string(email_template_name, c)
#         #             send_mail(subject, email,[user.email], to=[to_email],fail_silently=False)
#         #         result = self.form_valid(form)
#         #         messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
#         #         return result
#         #     result = self.form_invalid(form)
#         #     messages.error(request, 'This username does not exist in the system.')
#         #     return result
#         # messages.error(request, 'Invalid Input')
#         # return self.form_invalid(form)