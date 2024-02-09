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
