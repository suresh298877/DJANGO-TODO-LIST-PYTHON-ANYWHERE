from django.contrib import admin
from django.urls import path, include
from . import views

# for images


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('', views.landing_view, name='landing'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    path('gverify/<str:user_id>/', views.gverify_view, name='gverify'),
    path('add-todo/', views.add_todo_view, name='add_todo'),
    path('delete_todo/<int:id>', views.delete_todo_view, name='delete_todo'),
    path("change_status/<int:id>/<str:status>",
         views.change_todo_status, name='change_todo_status'),



    # rest framework url's
    # path('api-auth/',include('rest_framework.urls')),
    path('api/todolist/', views.todo_get_post),
    path('api/tododelete/<int:id>/', views.todo_delete),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# for images
