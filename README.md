# Django 데이터 적재 미션

## 📌 미션 개요

Django ORM을 활용하여 새로운 데이터 모델을 설계하고, 테스트 데이터 **1,000건을 자동 생성하여 데이터베이스에 적재**합니다.

Student 모델을 그대로 사용하는 것이 아니라 새로운 주제인 **도서(Book)** 모델을 직접 설계했습니다.

---

## 🎯 요구사항

- 새로운 Model 설계
- 최소 1,000건의 테스트 데이터 자동 생성
- 데이터를 수기로 작성하지 않고 반복문을 이용하여 생성
- Django ORM을 이용하여 정확히 1,000건이 적재되었는지 검증
- Template에서 적재된 데이터 일부 출력

---

## 1. Book 모델 설계

`books/models.py`

```python
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    published_date = models.DateField()
    stock = models.PositiveIntegerField()
```

도서 데이터를 표현하기 위해 다음 필드를 정의했습니다.

| 필드 | 설명 |
| --- | --- |
| `title` | 도서 제목 |
| `author` | 저자 |
| `price` | 가격 |
| `published_date` | 출판일 |
| `stock` | 재고 수량 |

모델 생성 후 migration을 진행합니다.

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 2. 테스트 데이터 1,000건 자동 생성

1,000건의 데이터를 직접 작성하지 않고 Python 반복문과 Django ORM의 `bulk_create()`를 이용하여 생성합니다.

`books_create_bulk.py`

```python
from datetime import date, timedelta
from books.models import Book


if Book.objects.count() == 0:
    books = [
        Book(
            title=f"테스트 도서 {i + 1}",
            author=f"작가 {i % 50 + 1}",
            price=10000 + i,
            published_date=date(2020, 1, 1) + timedelta(days=i),
            stock=i % 100,
        )
        for i in range(1000)
    ]

    Book.objects.bulk_create(books)

print(Book.objects.count())
```

`bulk_create()`를 사용하여 생성한 Book 객체들을 데이터베이스에 한 번에 효율적으로 적재합니다.

또한

```python
if Book.objects.count() == 0:
```

조건을 사용하여 데이터가 없는 경우에만 1,000건을 생성하도록 했습니다.

따라서 생성 스크립트를 여러 번 실행하더라도 기존 데이터가 존재하면 추가 데이터가 생성되지 않습니다.

---

## 3. 데이터 적재

Django 환경에서 생성 스크립트를 실행합니다.

```bash
python manage.py shell < books_create.py
```

또는 Django shell에 먼저 진입한 후 실행할 수도 있습니다.

```bash
python manage.py shell
```

```python
exec(open("books_create_bulk.py", encoding="utf-8").read())
```

---

## 4. ORM을 이용한 데이터 검증

Django shell을 실행합니다.

```bash
python manage.py shell
```

Book 모델을 불러옵니다.

```python
from books.models import Book
```

ORM의 `count()`를 이용하여 데이터 개수를 확인합니다.

```python
Book.objects.count()
```

결과:

```text
1000
```

이를 통해 데이터베이스에 정확히 **1,000건의 Book 데이터가 적재되었음**을 확인할 수 있습니다.

---

## 5. View에서 데이터 일부 조회

1,000건을 모두 화면에 출력하지 않고 일부 데이터만 조회합니다.

`books/views.py`

```python
from django.shortcuts import render
from .models import Book


def book_list(request):
    books = Book.objects.all()[:20]

    return render(
        request,
        "books/book_list.html",
        {"books": books},
    )
```

`[:20]`을 사용하여 전체 1,000건 중 **20건만 Template으로 전달**합니다.

---

## 6. URL 연결

`config/urls.py`

```python
from django.contrib import admin
from django.urls import path
from books.views import book_list


urlpatterns = [
    path("admin/", admin.site.urls),
    path('books/', book_list, name='book_list'), 
]
```

---

## 7. Template에서 데이터 출력
`books/views.py`
```
from django.shortcuts import render
from .models import Book

def book_list(request):

    books = Book.objects.all()[:20]
    print(books)

    return render(request, "books/list.html", { "books": books })
```


`books/templates/books/book_list.html`

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>도서 목록</title>
</head>
<body>
    <h1>도서 목록</h1>

    <table border="1">
        <thead>
            <tr>
                <th>제목</th>
                <th>저자</th>
                <th>가격</th>
                <th>출판일</th>
                <th>재고</th>
            </tr>
        </thead>

        <tbody>
            {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.price }}</td>
                <td>{{ book.published_date }}</td>
                <td>{{ book.stock }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5">등록된 도서가 없습니다.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

브라우저에서 `/books/`로 접근하면 데이터베이스에 적재된 Book 데이터 중 일부를 확인할 수 있습니다.

---

## 추가) 데이터 1000건에 대해 create와 bulk_create의 소요시간 비교
 `.\books_create_bulk.py 파일 시간 측정 기능 추가`
```python
import time
from books.models import Book
from datetime import date, timedelta

Book.objects.all().delete()
start_time = time.perf_counter()
if Book.objects.count() == 0:
    books = [
        Book(
            title=f"테스트 도서 {i + 1}",
            author=f"작가 {i % 50 + 1}",
            price=10000 + i,
            published_date=date(2020, 1, 1) + timedelta(days=i),
            stock=i % 100,
        )
        for i in range(1000)
    ]

    Book.objects.bulk_create(books)

end_time = time.perf_counter()
print(f"데이터 적재 시간: {end_time - start_time:.4f}초")
print(Book.objects.count())
```

`.\books_create_unit.py`
```python
import time
from books.models import Book
from datetime import date, timedelta

Book.objects.all().delete()

start_time = time.perf_counter()

for i in range(1000):
        Book.objects.create(
            title=f"테스트 도서 {i + 1}",
            author=f"작가 {i % 50 + 1}",
            price=10000 + i,
            published_date=date(2020, 1, 1) + timedelta(days=i),
            stock=i % 100,
        )

end_time = time.perf_counter()
print(f"데이터 적재 시간: {end_time - start_time:.4f}초")

print(Book.objects.count())
```

위 스크립트를 각각 3회 실행하여 평균값을 낸 결과, bulk_create는 0.0293초, create는 2.0666초로 소요 시간에서 약 70배의 차이가 났습니다..

---

## 🔎 Django ORM

ORM(Object-Relational Mapping)은 Python 객체와 데이터베이스의 테이블을 연결하여 SQL을 직접 작성하지 않고 Python 코드로 데이터베이스를 조작할 수 있도록 해주는 기능입니다.

이번 미션에서는 다음과 같은 Django ORM 기능을 사용했습니다.

```python
# 데이터 개수 조회
Book.objects.count()

# 전체 데이터 조회
Book.objects.all()

# 여러 데이터를 한 번에 생성
Book.objects.bulk_create(books)
```

예를 들어 SQL을 직접 작성하면:

```sql
SELECT COUNT(*) FROM books_book;
```

과 같은 작업을 Django ORM에서는 다음과 같이 사용할 수 있습니다.

```python
Book.objects.count()
```

---

## ✅ 최종 결과

이번 미션을 통해 다음 작업을 수행했습니다.

1. `Book` 모델 직접 설계
2. 반복문을 이용한 테스트 데이터 1,000건 자동 생성
3. `bulk_create()`를 이용한 대량 데이터 적재
4. `Book.objects.count()`를 이용한 1,000건 적재 검증
5. View에서 20건만 조회
6. Template에서 적재된 데이터 출력
