# React-Django-Blog

## Requirements
* Python 3.9
* PostgreSQL
* Node v.14.16.1
* npm 7.11.2
* Django

Set up your **.env** file to make changes to your backend settings.

### Local Run
1. Clone the repository into your evid project directory (alongside metastudies) and move into the directory: `git clone https://github.com/nicholasjuncos/React-Django-Blog.git` and `cd react-django-blog`. Add the **.env** file here in the backend project directory.
2. Run PostgreSQL and create a database. Name it and remember the name for your .env file.
3. Create a virtual environment with python 3.9: `python3.9 -m venv venv`
4. Activate environment: `source venv/bin/activate`
5. Install requirements: `pip install -r requirements/local.txt`
6. Setup your database with `python manage.py migrate`
7. Run your backend with `python manage.py runserver`
8. In the frontend, run `npm install`
9. Run your frontend with `npm start`
