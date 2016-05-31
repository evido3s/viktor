#!/bin/bash


SUCCESS="\033[;32;1m"
WARNING="\033[;33;1m"
DANGER="\033[;31;1m"
INFO="\033[;35;1m"
END="\033[0m"

PWD=`pwd`


if [ `uname -s` != "Linux" ];then
    printf "$DANGER This script only support CentOS7_x64 or later system.\n$END"
    exit 126
else
    printf "$WARNING You will support MySQL server, Redis and config the file.\n$END"
fi

read -p "Please Input your supervisor config dir:" SPWD
read -p "Please Input your bind ip :" BIP
read -p "Please Input your bind port:" BP
read -p "Please Input your error log dir:" ELPWD
read -p "Please Input your info log dir:" ILPWD

function Install() {
    echo_supervisord_conf > $PWD/supervisor.conf
    sed -i "s/bind = '127.0.0.1:5000'/bind = '$BIP:$BP'" $PWD/gunicorn_config.py
    echo "[program:celery]
    command=celery worker -A celery_worker.celery
    directory=$PWD
    autorestart=false
    stdout_logfile=$ELPWD/celery.log
    stderr_logfile=$ILPWD/celery.log" >> $PWD/supervisor.conf
    echo "[program:web]
    command=gunicorn manage:web -c $PWD/gunicorn_config.py
    directory=$PWD
    autorestart=false
    stdout_logfile=$ELPWD/gunicorn.log
    stderr_logfile=$ILPWD/gunicorn.err" >> $PWD/supervisor.conf
}

function nginx() {
    yum install epel-release -y
    yum install nginx -y
    echo "location / {
        pass_proxy http://$BIP:$BP;
    }" >> /etc/nginx/default.d/viktor.conf
    systemctl start nginx
}

printf "$INFO ============>> Start install... <<============\n$END"
Install
printf "$INFO ============>> Start supervisor... <<============\n$END"
supervisord -c $SPWD/supervisor.conf
printf "$INFO ============>> Start nginx... <<============\n$END"
nginx

if [ `echo $?` -eq 0 ];then
    printf "$SUCCESS Viktor start success.\n$END"
    printf "$SUCCESS =============>> OK! <<==============\n$END"
else
    printf "$DANGER Viktor start failed.\n$END"
fi
