#### Запуск проекта
```
docker compose up --build -d
```

Сервер запускается локально на адресе http://0.0.0.0:8000/

Админка доступна по адресу http://0.0.0.0:8000/, для авторизации в ней необходимо создать суперюзера с помощью команды
```
python manage.py createsuperuser
```

Для запуска тестов используется команда
```
python manage.py test
```

Также доступен свагер для доступа ко всем ендпоинтам проекта, он доступен по адресу http://0.0.0.0:8000/swagger/

Для регистрации нового юзера можно использовать роут /accounts/register/
В нем используется поле с изображениями, id которого нужно передать в поле avatar_id. Само изображение загружается через роут /accounts/images/upload/
При регистрации можно выбрать роль, worker или customer. Аватар необходим только для роли worker.
Права доступа пользователей к дополнительным функциям можно выдать только через админку в таблице Users
После регистрации неоходимо получить токен через роут /accounts/token/. Токен будет использоваться для дальнейшей авторизации в запросах

Для получения информации о пользователе используется роут /accounts/accounts/me/

Если пользователь залогинен как customer, то он будет иметь доступ к роуту /tasks/tasks/. Для создания новой задачи отправляется POST запрос, для получения созданных им задач GET
Если пользователь залогинен как worker, то он также будет иметь доступ к роуту /tasks/tasks/, но только к получению списка своих и не занятых другими задач.
Для обновления своих задач worker может использовать роут /tasks/tasks/{id}/
Для получения доступа к созданию и списку всех задач ему необходимо выдать права через админку

Для того, чтобы назначить себе задачу, worker-y необходимо отправить запрос на /tasks/tasks/assign/, в теле передается id никем не занятой задачи.
После успешного назначения задача меняет статус с to_do на in_progress

Для того, чтобы пометить свою задачу как выполненную, worker-y необходимо отправить запрос на /tasks/tasks/mark_as_completed/, в теле передается id задачи и обязательный отчет.
После завершения статус задачи меняется на completed и текущее время ставится как время закрытия задачи 

Если у worker-a есть права создания других работников или заказчиков, то он может использовать роут /accounts/accounts/create/
В него он должен передать данные нового юзера, аватар, если это будет worker, и роль, которая доступна ему для создания



