# Django Real Estate App With Multiple Users And Databases

This is a Django backend REST API using the Django REST Framework, that demonstrates how you can use multiple user types and multiple databses.

In order to test out this project, follow these steps:

- clone the repo

Then create 2 databases in postgreSQL, one called **listings_users** and one called **listings_listings**

Then under core/settings.py:

- find the DATABASES setting, set the PASSWORD field to both your databases password to your postgreSQL user password

Once you have your databases setup, proceed to the following steps:

- create a virtual environment by running: `python -m venv venv` or MacOS `python3 -m venv venv`
- then activate the virtual environment: source `venv/bin/activate` (MacOS) or `venv/Scripts/activate` (Windows)
- then run the following commands:
- `pip install -r requirements.txt`
- `python manage.py makemigrations`
- `python manage.py migrate user --database=users`
- `python manage.py migrate --database=users`
### To create a superuser:
- `python manage.py createsuperuser --database=users`
### then you can run the server by running: 
`python manage.py runserver`
