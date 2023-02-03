HOW TO INSTALL ON LINUX SYSTEM

#!/bin/bash
apt update
apt install -y python3-pip
pip3 install django
pip3 install djangorestframework
pip3 install pillow
git clone https://github.com/Timon-3/project-bravo.git
cd project-bravo/tst_room_booking/
python3 manage.py migrate
python3 manage.py runserver 0:8000
