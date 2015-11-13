用户登录

---admin

---user
-> 任务选择
-> 进入任务

Server url: 127.0.0.1:5000

## API Services##

### Index ###

```
#!python
http://SERVER/index/
method: None
function: show_entries
```
**Input**

session login status

**Output**

If session get login, return task.html else return login.html

### Login ###

```
#!python
http://SERVER/login/
method: 'POST'
function: login
```
**Input**

request.form['username']

request.form['passwd']

**Output**

if correct -> redirecturl index

else -> redirecturl login


### Task ###

```
#!python
http://SERVER/Task/
method: None
function: show_entries
```
**Input**

1. db
2. category_lis --> for exact english name

**Output**

json:

"id": {"name":xx,"status":xx}