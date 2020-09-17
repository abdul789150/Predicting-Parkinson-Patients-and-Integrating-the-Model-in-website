For running this project you will need following things

-> installation of django ( pip install django) 
-> installation of mysql client for django
-> install xampp ( lampp if using linux )

Then start xampp, and run phpmyadmin, and database, after that open up the browser and goto "localhost/phpmyadmin", now here create a new database with the name "parkinson_db"

 

Then first go inside the directory where you can find "migrations.py" file, open the terminal/command line within that directory and run the following commands

-> python manage.py makemigrations
-> python manage.py migrate

Then for loading FAQ's into database run the following commands

-> python manage.py loaddata /path-to/fixtures/topic.json
-> python manage.py loaddata /path-to/fixtures/faq.json 

After all that run the command below to run the website

->python manage.py runserver
