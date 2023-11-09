Создал таблицы и наполнил их данными из тз

```
CREATE TABLE full_names (
    name text PRIMARY KEY,
    status integer
);


CREATE TABLE short_names (
    name text PRIMARY KEY,
    status integer
);

INSERT INTO short_names (name, status) VALUES
    ('nazvanie1', 1),
    ('nazvanie2', 0),
    ('nazvanie5445', 1);

INSERT INTO full_names (name, status) VALUES
    ('nazvanie1.mp3', NULL),
    ('nazvanie5445.mp3', NULL),
    ('nazvanie3.mp3', NULL);
```

Сами запросы на обновление статуса таблицы full_names

вариант 1:
Выполняет отдельное обновление для каждой записи

```
UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE substring(fn.name from 1 for position('.' in fn.name) - 1) = sn.name;
```
вариант 2:
Создать временную таблицу

```
-- временная таблица
CREATE TEMP TABLE temp_table AS
SELECT fn.name AS full_name, sn.status
FROM full_names fn
JOIN short_names sn ON substring(fn.name from 1 for position('.' in fn.name) - 1) = sn.name;

-- обновление статуса в таблице full_names
UPDATE full_names fn
SET status = tb.status
FROM temp_table tb
WHERE fn.name = tb.full_name;

-- удаление временной таблицы
DROP TABLE temp_table ;
```

