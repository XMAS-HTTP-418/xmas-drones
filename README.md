# Запуск

## Linux / Mac
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python main.py
```

## Windows
```bash
python -m venv env
env/Scripts/Activate.ps1
pip install -r requirements.txt
python main.py
```

# Альтернативные сценарии
* Проверить взаимодействие на сокетах
```bash
python test_master.py
python test_slave.py
```

* Проверить визуализацию
```bash
python test_master.py
python test_slave.py
```
# Алгоритм

Поиск ближайшей точки - KD-TREE

Распределение ресурсов - Shortest augmenting path algorithm
Оптимальный путь - Алгоритм Дейкстры

# Библиотеки
Для работы с линейной алгеброй и более быстрой работой с массивами - numpy

Для обработки изображений - Pillow

Для визуализации - matplotlib

Форматирование кода - black, isort

# Python
Разработывался на версии 3.10

# Авторы:
[Егор Голубев](https://github.com/huscker)\
[Павел Ивин](https://github.com/pavivin)\
[Андрей Баранов](https://github.com/Nicialy)\
[Дмитрий Иванов](https://github.com/Demitry0-0)