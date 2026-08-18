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

# exec(open("books_create_bulk.py", encoding="utf-8").read())로 shell에서 실행