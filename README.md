# Cyber Security Base: Project

This repository contains the intentionally made vulneruble app that was developer for the project part of the [cyber security base 2024 course](https://cybersecuritybase.mooc.fi/module-3.1) by University of Helsinki. The app contains 5 different flaws from the [OWASP top ten list](https://owasp.org/www-project-top-ten/) as well as their fixes.

## Installation Instructions

1. Clone the app:

```
    git clone https://github.com/elessartech/cyber-security-project-todo.git
```

2. Install dependencies:
```
    pip install -r requirements.txt
```

3. Apply database migrations:
```
    python manage.py makemigrations
    python manage.py migrate
```

4. Run the server:
```
    python manage.py runserver
```

## Flaws

### 1. Injection

[exact source link pinpointing flaw 1](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/views.py#L34)

[exact source link pinpointing fix for the flaw 1](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/views.py#L31)

Injection refers to a set of security vulnerabilities where an intruder is able to insert potentially malicious data or code into the applications ecosystem. It may be performed via for example unauthorized access, data manipulation or the execution of commands that are not to be executed in a particular scenario. The main purpose of injection intrusions is to exploit app vulnerabilities and achieve the execution of unintended and potentially harmful actions.

For this application, the deletion of the created todos may be vulnerable for the SQL-injection attack. It is designed to select and fetch all corresponding todos from the database relying on the string interpolation to construct the SQL query: `Todo.objects.raw(f"SELECT * FROM todo_todo WHERE id={item_id};")`. This approach can introduce severe injection vulnerabilities, so that an attacker could manipulate the `item_id` variable to execute arbitrary SQL code, which may cause the deletion of unwanted objects in the database.

The aforementioned can be fixed by using the Django ORM with parameterized queries like `Todo.objects.get(id=id_value, creator=request.user)`. In this case, such approach would provide higher level of security by automatically handling the generation and parameterization of SQL-queries by escaping and quoting user provided values and as a result majorily reducing the risk of injection vulnerabilities.

### 2. Broken Authentication

[exact source link pinpointing flaw 2(whole user_login() function)](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/views.py#L53)

[exact source link pinpointing fix for the flaw 2](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/views.py#L52)

Broken authentication refers to security vulnerability in the app logics responsible for user authentication and session handling. It can lead to severe security breaches such as unauthorized access to app user accounts, identity disclosure etc. One common scenario is when an intruder can brute force user credentials by exploiting not defensive enough authentication mechanisms. If the application allows unlimited number of login attempts, it may be potentially vulnerable to such attacks, since then an attacker can be endlessly trying various combinations until the correct one is found.

The `@ratelimit` decorator in Django apps can be used to mitigate brute force attacks by limiting the rate at which login attempts can be made from a certain IP. By applying such decorator the authentication mechanism enforces a limit on the number of login attempts within a specific timeframe, which makes it seriously more difficult for an intruder to breach the login succesfully. The string `@ratelimit(key='ip', rate='5/m', method='POST', block=True)` allows 5 login attempts per minute and if this limit is exceeded, any subsequent requests are getting blocked. 

### 3. Broken Access Control

[exact source link pinpointing flaw 3](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/views.py#L22)

[exact source link pinpointing fix for the flaw 3(start)](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/forms.py#L14)

[exact source link pinpointing fix for the flaw 3(end)](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/forms.py#L21)

Broken Access Control is a security vulnerability that occurs when an app allows users to perform actions or access resources that they should not be authorized to operate with. It may happen when the access control mechanisms are not properly adjusted, what may lead to potential security breaches. 

For this application in particular, there is a form that can be found on the user page once authorized, that allows users to create todo tasks. Initially, the code does not contain any authentication checks, meaning that any user, whether authenticated or not, can submit data to create a Todo item. Additionally, the user validation checks are also missing. Without these checks, there's no verification that the user submitted as the Todo item creator actually exists in the system. The aforementioned may potentially lead to the code allowing the creation of Todo items without properly verifying the user's identity or checking if the user has the necessary permissions, signifying the Broken Access Control-vulnerability.

Therefore, this issue can be mitigated by installing additional authentications checks and verifications. Thus, intruders will no longer be capable of exploiting this misconfiguration and prevent the unauthorized users from creating Todo items and this way violating proper access controls.

### 4. Security Misconfiguration

[exact source link pinpointing flaw 4](https://github.com/elessartech/cyber-security-project-todo/blob/main/cybersecurityprojecttodo/settings.py#L23)

[exact source link pinpointing fix for the flaw 4](https://github.com/elessartech/cyber-security-project-todo/blob/main/cybersecurityprojecttodo/settings.py#L19)

Security misconfiguration refers to security vulnerability that occurs when a system or application is not securely configured. For example if the default software configuration has not been prepared for the production mode or if the error handling mechanism is established ineffectively, all such misconfiguration failures may subsequently lead to vulnerabilities in the security control of the application. 

In the situation of this application, there is the default secuity configuration that can be found in `settings.py`-file and such configuration variables as `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` are purposefully declared in an insecure manner. 

First of all, the `SECRET_KEY` is a critical component for cryptographic signing and supposed to be kept confidential. Setting it to a constant value like `"MY_SECRET_KEY"` makes it quite predictable and therefore guessable and attainable for intruders. A secret key if exposed can lead to vulnerabilities, such as session hijacking or data tampering. Thus, a good method to mitigate that would be to generate a random and complex key and provide it via environment variable.

Then, having `DEBUG` set to `True` in a production environment can expose sensitive application information to potential intruders. Detailed errors and their traces are displayed when an unhandled exception occurs, revealing internal details of the application and making it easier for intruders to identify and exploit vulnerabilities. Thus, for mitigation purposes `DEBUG` is supposed to be set to `False` when the app is deployed to production. 

Eventually, allowing any host `["*"]` in the `ALLOWED_HOSTS` parameter setting is also very risky. This setting is used to define a list of valid domains for the application. Allowing any host means that the application will respond to requests from any domain, potentially opening it to DNS rebinding attacks as well as other security risks. Strictly actual domain names or IP addresses that the application is expected to serve are to be defined in `ALLOWED_HOSTS `.

### 5. Sensitive Data Exposure

[exact source link pinpointing flaw 5](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/views.py#L34)

[exact source link pinpointing flaw 5(template)](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/templates/index.html#L15)

[exact source link pinpointing fix for the flaw 5](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/views.py#L29)

[exact source link pinpointing fix for the flaw 5(template)](https://github.com/elessartech/cyber-security-project-todo/blob/main/todo/templates/index.html#L16)

Sensitive Data Exposure is a type of vulnerability by exploiting which an intruder may get access to various kinds of sensitive information such as personal identification data, financial information, authentication credentials or any other information that, if disclosed, may lead to harm or unauthorized access.

For this application, it is possible for users to delete their created todos by clicking onto `Remove`-button. However, the delete action is triggered by `<a>` element with an `href` attribute pointing to the delete endpoint, where the sensitive information such as the item ID, is visible in the browser's address bar. In addition to that, the item ID is very predictable, meaning that it is just an integer number that gets incremented by 1 each time a new todo is saved in the database. All the aforementioned can lead to serious security vulnerabilities for an instance if an attacker manipulates the URL parameters and inserts some malicious Javascript code in there, especially taking into an account that CSRF protection is not applied for the GET-requests.

In order to fix that, there are such practices to introduce as making the delete action triggered by a `<form>` element with the method set to POST simultaneusly including item ID as a hidden input field, which will subsequently also hide any sensitive information from exposure in the URL. The use of a form will also protect against Cross-Site Request Forgery attacks by including the CSRF token `{% csrf_token %}` in the form. Additionally, would be beneficial to generate item IDs as random strings making them much less predictable for intruders.

