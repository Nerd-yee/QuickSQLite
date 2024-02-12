# QuickSQLite
A basic python-sql interface. WARNING, this is not secure (yet) do not use on anything important.
This is my first project that I am actually taking kind of seriously so any helpfull tips or point outs to dumb code would be very well appreciated

basic how to use (full documentation coming later):
open database with the Database class
```python
database = Database("Database_path")
```

custom queries can be run using the query method
```python
data = database.query("MYSQLQUERY", save_data=True)  # set save_date=True if you want method to return data, False if not
```

the select method has four inputs
1. columns
2. table
3. where
4. clause

the request is formated as
SELECT clause columns FROM table WHERE where
<br>
the clause is for select statements like ```SELECT DISTINCT```

for the query ```SELECT movies FROM table```:
```python
data = database.select("movies", "table")
```
by default the where is set to 1=1

for the query ```SELECT * FROM table WHERE id=5```:
```python
data = database.select("*", "table", "id=5")
```

for the query ```SELECT DISTINCT movies FROM table```
```python
data = database.select9"*", "table", clause="DISTINCT"
```

