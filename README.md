# WoofBook documentation #

### Установка и разворачивание среды ###

Создаем окружение:
```shell script
python3 -m venv путь_который_хотим
source путь_который_хотим
```
Далее устанавливаем зависимости
```shell script
pip install -r requirements.txt
```

### Поддержка языков
Создать язык
```shell
./manage.py makemessages -l ru_RU
```
Обновить все языки
```shell
./manage.py makemessages -a
```
Собрать новый файл, после перевода
```shell
./manage.py compilemessages
```

