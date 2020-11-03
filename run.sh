git checkout -- .
git checkout master
git pull origin master
pip3 install -r requirements.txt
setsid nohup flask run --host 0.0.0.0 --port 8080 --cert /etc/letsencrypt/live/gametime-server.hubermjonathan.com/fullchain.pem --key /etc/letsencrypt/live/gametime-server.hubermjonathan.com/privkey.pem &

