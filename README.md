# Анализ эффективности работы разработчиков

Пример запуска:

~~~sh
$ python3 main.py --files employees1.csv employees2.csv --report performance
    position               performance
--  -------------------  -------------
 1  Backend Developer             4.83
 2  DevOps Engineer               4.80
 3  Fullstack Developer           4.70
 4  Data Engineer                 4.70
 5  Frontend Developer            4.65
 6  Data Scientist                4.65
 7  Mobile Developer              4.60
 8  QA Engineer                   4.50
~~~

Проверка покрытия кода тестами:

~~~sh
$ pytest --cov=src tests/
...
Name              Stmts   Miss  Cover
-------------------------------------
src/database.py      12      0   100%
src/reports.py       44      3    93%
-------------------------------------
TOTAL                56      3    95%
~~~
