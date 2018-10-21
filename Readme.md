## Flask Base

Flask base is a basepoint starter project. How any times have you stared a new project, and had to recreate user creation, login, and forgot password?  I know I've done it a lot for different places I've worked.  I also know that I really don't want to have to do it anymore.  Therefore I created this repository with a base flask application that contains the initial bits you need to get going.  It allows you to come in and have a starting point.  You can then add or remove from what exists.

How to get started.
###

1) Flask Base is built on Python 3.x, so make sure that you have it available on your local machine.
2) Install virtualenv if you don't have it installed already.
3) Clone this repository to your local machine.
4) cd flask_base and then virtualenv -p python3 .
5) source ./bin/activate

6) Make sure docker is installed and running.
7) ```docker-compose up -d``` this will bring up mysql on port 3315 so you have a database.
8) Run ```flask db upgrade``` to build your database from the migration files.

9) ```python app.py``` to start the python development webserver