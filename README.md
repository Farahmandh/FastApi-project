## Запуск приложения

Собрать и запустить докер образ

```bash
docker-compose up -d
```

Прогнать миграции
```bash
docker-compose exec web alembic revision --autogenerate -m "Initial migration"

docker-compose exec web alembic upgrade head
```

## Авторизация и аутентификация пользователя

1) Создаем юзера
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

Я уже запускал код, так что мой ответ программы: `{"detail":"Username already registered"}`

2) Авторизация для получения токена:
```bash
curl -X POST "http://localhost:8000/users/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

Ответ:

`json{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp...", "token_type":"bearer"}
`

Копируем токен, он еще понадобится для запросов

3) Получаем инфу о юзере:

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

В моем случае:
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0Njk5NTY2N30.5r7rmnVweyW5PJEqv73AMvvmSk3euvTnbjwB0HcPS9U"
```

Ответ:
```json
{
    "email":"test@example.com",
    "username":"testuser",
    "id":1,
    "is_active":true,
    "is_admin":false,
}
```


## Управление категориями

1) Создаем категорию

```bash
curl -X POST "http://localhost:8000/categories/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fiction",
    "description": "Fictional literature"
  }'
```

Ответ:

```json
{
    "name":"Fiction",
    "description":"Fictional literature",
    "id":2,
}
```

2) Получаем список всех категорий

```bash
curl -X GET "http://localhost:8000/categories/"
```

Ответ:
```json
[
    {
        "name":"Fiction",
        "description":"Fictional literature",
        "id":1,
    },
    {
        "name":"Fiction",
        "description":"Fictional literature",
        "id":2,
    }
]
```

3) Получаем отдельную категорию

```bash
curl -X GET "http://localhost:8000/categories/1"
```

4) Обновляем категорию

```bash
curl -X PUT "http://localhost:8000/categories/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fiction & Fantasy",
    "description": "Fictional and fantasy literature"
  }'
```

Ответ:

```json
{
    "name":"Fiction & Fantasy",
    "description":"Fictional and fantasy literature",
    "id":1,
}
```

## Авторы

Тут все аналогично

1) Создание

```bash
curl -X POST "http://localhost:8000/authors/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "J.K. Rowling",
    "bio": "British author known for the Harry Potter series"
  }'
```

2) Получение

```bash
curl -X GET "http://localhost:8000/authors/"
```

3) Получение одного автора

```bash
curl -X GET "http://localhost:8000/authors/1"
```

4) Обновление

```bash
curl -X PUT "http://localhost:8000/authors/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "J.K. Rowling",
    "bio": "British author best known for the Harry Potter fantasy series"
  }'
```

## Книги

1) Создание книг

```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter and the Philosopher'\''s Stone",
    "description": "The first novel in the Harry Potter series",
    "publication_date": "1997-06-26",
    "isbn": "9780747532699",
    "price": 15.99,
    "rating": 4.8,
    "author_id": 1,
    "category_id": 1
  }'
```

```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "A Brief History of Time",
    "description": "A book about modern physics for the general reader",
    "publication_date": "1988-03-01",
    "isbn": "9780553380163",
    "price": 18.99,
    "rating": 4.5,
    "author_id": 2,
    "category_id": 2
  }'
```

```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter and the Chamber of Secrets",
    "description": "The second novel in the Harry Potter series",
    "publication_date": "1998-07-02",
    "isbn": "9780747538486",
    "price": 16.99,
    "rating": 4.7,
    "author_id": 1,
    "category_id": 1
  }'
```

Получение и обновление аналогично

## Рекомендации

1) Получите рекомендации по бронированию на основе ваших предпочтений

```bash
curl -X POST "http://localhost:8000/recommendations/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_categories": [1],
    "preferred_authors": [1],
    "min_rating": 4.5
  }'
```

## Удаление

1) Удаление книг

```bash
curl -X DELETE "http://localhost:8000/books/3" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

```bash
# First, delete all books by this author
# Then delete the author
curl -X DELETE "http://localhost:8000/authors/2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

```bash
# First, delete all books in this category
# Then delete the category
curl -X DELETE "http://localhost:8000/categories/2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```


## Тесты

Запуск тестов:

```bash
docker-compose exec web pytest
```

## Проверка состояния дб

```bash
docker-compose exec db psql -U postgres -d book_catalog
```

```sql
-- List all tables
\dt

-- Check users
SELECT * FROM users;

-- Check authors
SELECT * FROM authors;

-- Check categories
SELECT * FROM categories;

-- Check books
SELECT * FROM books;

-- Check relationships
SELECT b.title, a.name as author, c.name as category
FROM books b
JOIN authors a ON b.author_id = a.id
JOIN categories c ON b.category_id = c.id;
```

## Контейнеры

1) Перезапуск

```bash
docker-compose down
docker-compose up -d
```

2) Сброс бд и перезапуск

```bash
docker-compose down -v  # This will remove volumes
docker-compose up -d
docker-compose exec web alembic revision --autogenerate -m "Initial migration"
docker-compose exec web alembic upgrade head
```