## Files are inside main folder

## How to run?
0) go inside folder
1) [docker build -t main .]
2) [docker run -p 8000:8000 main]  



## Activate pip enviroment 
source /Users/danielfernandes/.local/share/virtualenvs/django_docker_demo-fWAxXL5O/bin/activate

## PYMONGO (connecting to databasem inside django app)
python -m pip install 'pymongo[snappy,gssapi,srv,tls]'

sudo pip install 'pymongo[snappy,gssapi,srv,tls]' -t /usr/local/lib/python3.10.4/site-packages/

python -m pip install dnspython

see changes in real time 
python manage.py runserver

https://www.youtube.com/watch?v=qWYx5neOh2s