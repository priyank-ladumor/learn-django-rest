<!-- virtual env create  -->
python -m venv .venv

<!-- virtual env activate (Git-Bash) -->
source .venv/Scripts/activate  

<!-- virtual env deactivate (Git-Bash) -->
deactivate

<!-- install Django  -->
pip install django

<!-- for create django server project -->
django-admin startproject myProject
cd myProject

<!--  Check version  -->
django-admin --version

<!-- Run the development server -->
python manage.py runserver

<!-- Run the development server using specific port for all network  -->
python manage.py runserver 0.0.0.0:9000

 <!-- Create a Django App -->
 <!-- Inside your project folder (where manage.py is) -->
python manage.py startapp any_name_want

 <!-- for creating requirements.txt -->
pip freeze > requirements.txt 

 <!-- for installing requirements.txt -->
pip install -r requirements.txt 

 <!-- how to remove all the packages in a virtual env -->
pip uninstall -r requirements.txt -y

<!-- tailwin install -->
pip install django-tailwind
<!-- for browser reload  -->
pip install django-browser-reload

<!-- init tailwind command code -->
python manage.py tailwind init

<!-- tailwind install on manage.py  -->
python manage.py tailwind install

<!-- start tailwind   -->
python manage.py tailwind start

<!-- create super user -->
python manage.py createsuperuser

<!-- reset super-user password -->
python manage.py changepassword your_superuser_username

<!-- make-migrations  -->
python manage.py makemigrations app_name

<!-- make-migrations (changes to a model and aren’t sure which app to use) -->
python manage.py makemigrations

<!-- database migrations in Django command  -->
python manage.py migrate

<!-- for create django-rest-framework  -->
pip install djangorestframework

