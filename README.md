# Django REST API - Аутентификация и Профили

Этот проект построен на базе Django REST Framework и использует JWT-аутентификацию. Основные возможности проекта включают регистрацию пользователей, вход, подтверждение email, сброс пароля, просмотр профиля и другие функции.

## Технологии

- Django и Django REST Framework
- Simple JWT
- SQLite (или другая база данных)
- djoser или кастомные сериализаторы для аутентификации (при необходимости)

---

## API Endpoint'ы

### 🔐 Аутентификация

| Endpoint                                   | Назначение                                                           |
|--------------------------------------------|----------------------------------------------------------------------|
| `POST /auth/register/`                     | Регистрация нового пользователя                                      |
| `POST /auth/verify-email/`                 | Подтверждение email (с использованием токена)                        |
| `POST /auth/login/`                        | Авторизация и получение JWT-токена                                     |
| `POST /auth/token/refresh/`                | Обновление токена                                                    |
| `POST /auth/logout/`                       | Выход из системы (аннулирование токена, занесение в blacklist)         |
| `POST /auth/password-reset/`               | Отправка email для сброса пароля                                       |
| `POST /auth/password-reset/confirm/`       | Сброс пароля с использованием токена                                  |

---

### 👤 Пользователи

| Endpoint               | Назначение                                             |
|------------------------|--------------------------------------------------------|
| `GET /users/me/`       | Получение информации о текущем пользователе            |

---

### 🧑‍💼 Профили

| Endpoint                                      | Назначение                                         |
|-----------------------------------------------|----------------------------------------------------|
| `GET /profiles/{username}/`                    | Просмотр профиля пользователя                      |
| `GET /profiles/me/`                            | Просмотр собственного профиля                        |
| `POST /profiles/{username}/follow/`            | Начало подписки на пользователя                   |
| `POST /profiles/{username}/unfollow/`          | Отмена подписки на пользователя                   |
| `GET /profiles/{username}/followers/`          | Список подписчиков пользователя                    |
| `GET /profiles/{username}/following/`          | Список пользователей, на которых подписан          |

---

## Установка

Клонируйте репозиторий и установите зависимости:

```bash
git clone https://github.com/Ali050617/Sprint.git
cd Sprint
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Выполнение миграций

```
python manage.py migrate
```

## Создание суперпользователя

``` 
python manage.py createsuperuser
```

## Автор

- [Nayimjonov](https://github.com/Nayimjonov)


