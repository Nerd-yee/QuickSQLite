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
<br>
<br>
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
data = database.select("*", "table", clause="DISTINCT")
```
For the query ```SELECT * FROM table ORDER BY movie DESC```:
```python
data = database.select("*", "table", "movie DESC")
```

in order to do a basic join the ```select_join``` method can be used
The query
```SQL
SELECT table1.id, table2.movie
FROM table1, table2
WHERE table1.id = table2.id
```
QuickSQLite accepts the inputs for columns and tables as a list as such:
```python
data = database.select_join(["table1.id", "table2.movie"], ["table1", "table2"], "table1.id = table2.id")
```

to use the ```GROUP BY``` clause:
```python
data = database.select_join(["table1.id", "table2.movie"], ["table1", "table2"], "table1.id = table2.id", group="table2.movie")
```
similarly with ```HAVING``` clause:
```python
data = database.select_join(["table1.id", "table2.movie"], ["table1", "table2"], "table1.id = table2.id", group="table2.movie", having="count(table2.movie) > 1")
```
<br></br>
<br></br>
In order to update a table with query:
```SQL
UPDATE table 
SET (movie='star treck') 
WHERE movie = 'star wars'
```
the code is:
```python
database.update("table", ["movie"], ["star treck"], "movie = 'star wars'")
```

to delete from a table:
```python
database.delete("table", "id > 100")
```
if only the table is given to the method or it is None it will drop the table 
to insert to table
```python
database.insert("table", ["column1", "column2"], ["data1", "data2"]
```
