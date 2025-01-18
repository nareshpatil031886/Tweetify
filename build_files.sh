echo "BUILD START"
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
echo "BUILD END"
apt-get update
apt-get install -y libmysqlclient-dev pkg-config
