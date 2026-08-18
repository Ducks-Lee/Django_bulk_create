"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# students 폴더 하위의 views.py 내부에 정의된 students_list 함수를 이 파일에서 호출할 수 있도록 참조
from students.views import student_list
from books.views import book_list

# urlpatterns에 접속 주소를 지정한다면, 해당 주소로 사용자가 접속했을 때, 실행할 로직을 지정할 수 있습니다.
urlpatterns = [
    path('admin/', admin.site.urls),

    # 127.0.0.1:8000/students/ 접속 시, 2번째 파라미터로 넣은 함수가 실행된다.
    path('students/', student_list, name='students_list'), 
    path('books/', book_list, name='book_list'), 
]
