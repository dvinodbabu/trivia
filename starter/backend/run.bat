call dev\Scripts\activate
set FLASK_APP=flaskr
set FLASK_DEV=development
start "1" python -m flask run
start "2" call frontend\npm install
pause