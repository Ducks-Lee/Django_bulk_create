from django.shortcuts import render
# 서버주소/students/ 접속 시, 실행해줄 함수

# HttpResponse는 응답을 text로 반환해주는 함수이다.
# from django.http import HttpResponse

from .models import Book

# 서버주소/students/ 접속 시, 실행해줄 함수
# 접속 시 수행해줄 로직을 작성하는 함수는 request가 필수 파라미터로 적혀야한다.
def book_list(request):

    # Student.objects.all() -> SELECT * FROM students의 SQL 쿼리문과 동일
    books = Book.objects.all()[:20]
    print(books)

    # render(request, "결과화면.html", { 변수명: 화면으로 보낼 데이터 })
    # 루트폴더/templates/list.html 파일이 타겟이 됩니다.
    # 다만, 이렇게 루트 폴더 하위 templates에 넣으면 무슨 용도로 쓰는건지 부정확하기 때문에
    # 실제로는 teamplates 폴더 하위에 개별 app 폴더를 하나 더 생성합니다.
    # 어플리케이션명/list.html 으로 하면 보다 용도가 명확합니다.
    return render(request, "books/list.html", { "books": books })
    # 마지막 파라미터는 딕셔너리로 함수 내 데이터를 브라우저 화면으로 전송합니다.

    # HttpResponse는 응답을 text로 반환해주는 함수이다.
    # return HttpResponse("/students 접속 확인")
    