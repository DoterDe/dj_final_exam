from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include,re_path
from app.views import email_massage,home, DeletePost, CreatePost,APIProductViewSet,APIREADProductViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LogoutView
from core.settings import DEBUG
from app.views import register_and_login_view ,logout_student , enter_confirmation_code, register, profile_view , profile_update_view , like_post , post_list , notification

router = DefaultRouter()
router.register('product', APIProductViewSet)
router1 = DefaultRouter()
router1.register('product1', APIREADProductViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('email/' , email_massage, name='email_massage'),
    path('post_list/', post_list, name='home'),
    path('post/<int:post_id>/', post_list, name='post_list_or_detail'),
    path('like/<int:post_id>/', like_post, name='like_post'), 
    path('create_post/', CreatePost.as_view(), name='create'),
    path('delete/<int:id>', DeletePost.as_view(), name='delete'),
    path('', home , name = 'home_not_log'),
    # path('api/',api_product, name='api' ),
    # path('api_id/<int:pk>/', api_product_id, name='api_id'),
    path('api_product/', include(router.urls)),
    path('api_read', include(router1.urls)),
    path('logout/', logout_student , name='logout'),    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-and-login/', register_and_login_view, name='register_and_login'),
    path('register//<int:user_id>/',register, name='register' ),
    path('enter_confirmation_code/<int:user_id>/', enter_confirmation_code, name='enter_confirmation_code'),
    path('profile/', profile_view , name='profile'),
    path('profile/update/', profile_update_view, name='profile_update'),
    # path('api/',APIProduct.as_view(), name='api' ),
    # path('api_id/<int:pk>/', APIProductDetail.as_view(), name='api_id')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
