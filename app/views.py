
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.shortcuts import render,redirect ,get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CreatePostForm , UserForm , FormLogin, FormReg , CodeForm,Register , UserProfileForm , CommentForm
from .models import UserProfile1,Product,Post , Like
from django.views.generic.edit import CreateView, DeleteView
from .serializers import ProductSerializers
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate
import random
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
import logging

def generate_code():
    random.seed()
    return str(random.randint(10000,99999))

def register_and_login_view(request):
    signup_form = FormReg()
    login_form = FormLogin()

    if request.method == 'POST':
        if 'signup_submit' in request.POST:
            signup_form = FormReg(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.is_active = False 
                user.code = generate_code()  
                user.save()  

                code = user.code  
                message = f'Ваш код подтверждения: {code}'
                send_mail(
                    'Код подтверждения',
                    message,
                    settings.EMAIL_HOST_USER,
                    [signup_form.cleaned_data['email']],
                    fail_silently=False
                )

                return redirect('enter_confirmation_code', user_id=user.id) 

        elif 'login_submit' in request.POST:
            login_form = FormLogin(request=request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли в систему.')
                    return redirect('home')
                else:
                    messages.error(request, "Аутентификация не удалась: неверное имя пользователя или пароль.")
            else:
                messages.error(request, "Форма входа недействительна. Пожалуйста, исправьте ошибки ниже.")

    return render(request, 'authenticate/register_and_login.html', context={'signup_form': signup_form, 'login_form': login_form})

def enter_confirmation_code(request, user_id):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code_use = form.cleaned_data.get("key")
            try:
                user = UserProfile1.objects.get(id=user_id)
                if user.code == code_use:
                    user.is_active = True 
                    user.code = generate_code() 
                    user.save()
                    login(request, user)
                    messages.success(request, 'Ваш аккаунт успешно подтверждён.')
                    return redirect('register', user_id=user.id)
                else:
                    form.add_error(None, 'Неверный код подтверждения.')
            except UserProfile1.DoesNotExist:
                form.add_error(None, 'Пользователь не найден.')
    else:
        form = CodeForm()

    return render(request, 'authenticate/enter_code.html', {'form': form})

def register(request, user_id):
    user = UserProfile1.objects.get(id=user_id) 
    if request.method == 'POST':
        form = Register(request.POST, request.FILES, instance=user)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация завершена успешно.')
            return redirect('home')
        else:
            messages.error(request, "Ошибка при регистрации. Пожалуйста, исправьте ошибки ниже.")
    else:
        form = Register(instance=user)

    return render(request, 'authenticate/register.html', {'form': form}) 


@login_required
def profile_view(request):
    posts = Post.objects.filter(author=request.user)
    user_profile = UserProfile1.objects.get(id=request.user.id) 
    form = UserProfileForm(instance=user_profile)  
    return render(request, 'profile.html', {'form': form, 'profile': user_profile , 'posts': posts})
logger = logging.getLogger(__name__)
@login_required
def profile_update_view(request):
    user_profile = get_object_or_404(UserProfile1, id=request.user.id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)


        try:
            if form.is_valid():
                form.save()
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')

                if password1 and password1 == password2:
                    user = request.user
                    logger.info(f"User before password change: {user.username}, ID: {user.id}")
                    user.set_password(password1)
                    user.save()

                    logger.info("Updating session auth hash.")
                    update_session_auth_hash(request, user)
                    logger.info("Session auth hash updated successfully.")

                messages.success(request, 'Изменения сохранены успешно!')
                return JsonResponse({'success': True})
           
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
            

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form})
 
class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'create_post.html'
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

@login_required
def notification(request): 
    username=request.user.username 
    user=UserProfile1.objects.get(username=username) 
 
    notification = list(user.likes_author.all()) + list(user.reviews_author.all()) 
     
    notification = sorted(notification, key=lambda x: x.created_at, reverse=True) 
 
    return render(request, 'notification.html', {'notification': notification})

@permission_classes((IsAuthenticated,))
class APIProductViewSet(ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializers


class APIREADProductViewSet(ReadOnlyModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = (IsAuthenticated,)

# class APIProduct(generics.ListAPIView):
#     queryset =  Product.objects.all()
#     serializer_class = ProductSerializers

# class APIProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset =  Product.objects.all()
#     serializer_class = ProductSerializers



# @api_view(['GET', 'POST'])
# def api_product (request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializers(products, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializers(data=request.data) 
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE']) 
# def api_product_id(request, pk): 
#     rubric = Product.objects.get(pk=pk) 
#     if request.method == 'GET': 
#         serializer = ProductSerializers(rubric) 
#         return Response(serializer.data) 
#     elif request.method == 'PUT' or request.method == "PATCH": 
#         serializer = ProductSerializers(rubric, data=request.data, partial = True) 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
#     elif request.method == 'DELETE': 
#         rubric.delete() 
#         return Response ('Success delete',status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def api_rubrics(request) : 
#     if request.method == 'GET':
#         rubrics = Product.objects.all() 
#         serializer = RubricSerializer (rubrics, any-Irel retumn Response (serializer.data) elif request.method = 'POST': serializer = RubricSerializer (data=request .data) if serializer.is valid(): serializer.save () return Response (serializer.data, status=status.HTTP 201 CBATED return Response (serializer.errors, status-status.HITP 400 BAD REQUEST]

@login_required
def post_list(request):
    posts = Post.objects.all()
    user_liked_post_ids = Post.objects.filter(likes__user=request.user.id).values_list('id', flat=True)

    form = CommentForm()

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  
            comment.author = request.user  
            comment.save()  
            return redirect('home') 

    context = {
        'posts': posts,
        'user_liked_post_ids': list(user_liked_post_ids), 
        'form': form,
    }
    return render(request, 'post_list.html', context)
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:  
            like.delete()

    return redirect('home') 


def home(request):
    posts=Post.objects.all()

    return render(request, 'home.html', context= {'posts':posts } )

# @api_view(['GET'])
# def api_product(request):
#     if request.method == 'GET':
#         product = Product.objects.all()
#         serializer = ProductSerializers(product, many = True)
#         return Response(serializer.data)
# @api_view(['GET'])
# def api_product_id(request, pk):
#     if  request.method == 'GET':
#         product = Product.objects.get(pk=pk)
#         serializer = ProductSerializers(product)
#         return Response(serializer.data)






def email_massage(request):
    user = UserProfile1.objects.get(id=1)
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        [f"{user.email}"],
        fail_silently=False,
    )
    return HttpResponseRedirect("/")



class DeletePost(DeleteView):
    model = UserProfile1   
    success_url = reverse_lazy('home')
    template_name = 'delete.html'

@login_required
def logout_student(request):
    logout(request)
    return render(request, 'home.html')