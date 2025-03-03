# rishat_test_app

# Django Shop Application

## 1. Настройка `.env` файла

Перед запуском проекта необходимо создать `.env` файл в корневой директории. Для удобства уже имеется файл `.env_empty` с перечисленными переменными без значений.

### **Создание .env**
Скопируйте `.env_empty` в `.env`:
```sh
cp .env_empty .env
```

### **Заполните переменные в `.env`**
В файле `.env` должны быть указаны следующие переменные:
- `SECRET_KEY` – секретный ключ Django.
- `STRIPE_SECRET_KEY` – секретный ключ Stripe.
- `STRIPE_PUBLIC_KEY` – публичный ключ Stripe.
- `DEBUG` – режим отладки (True/False).

**Генерация `SECRET_KEY`**:
```sh
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Другие переменные должны быть заполнены вручную (например, из кабинета Stripe).

---

## 2. Запуск проекта с помощью Docker

Используйте следующую команду для сборки и запуска контейнера:
```sh
docker build -t test_app . && docker run -v sqlite_volume:/app/db_data -p 8000:8000 --name test_app_container -d test_app
```

Эта команда:
- Собирает образ с тегом `test_app`.
- Запускает контейнер `test_app_container`.
- Прокидывает volume `sqlite_volume` для хранения базы данных `db.sqlite3`.
- Открывает порт `8000`.

---

## 3. Создание суперпользователя

Для создания суперпользователя выполните:
```sh
docker exec -it test_app_container ./manage.py createsuperuser
```
Затем следуйте инструкциям для ввода логина, email и пароля.

---

## 4. Добавление товаров

Для добавления товаров:
1. Откройте админ-панель: `http://localhost:8000/admin/`
2. Войдите под суперпользователем.
3. Перейдите в раздел `Item`.
4. Добавьте новый товар, указав название, описание и цену.

---

## 5. Описание работы приложения

Приложение представляет собой магазин с возможностью оплаты через Stripe.

### **Основные функции**:
- Эндпоинт `item/<int:item_id>` отображает страницу с описанием товара.
- На странице есть кнопки `Купить сейчас` и `Добавить в корзину`.
- При добавлении в корзину создаётся запись в `Order`.
- При нажатии `Оплатить корзину` или `Оплатить сейчас` происходит редирект на страницу оплаты Stripe.
- ID текущего заказа хранится в `cookie`, позволяя добавлять товары в корзину.

После успешной оплаты заказу проставляется дата завершения `finished_at`.

---
