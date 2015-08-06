ps -ef | grep [r]edis-server | awk -F ' ' '{print$2}' | xargs kill -9

exec redis-server > /dev/null 2>&1 &

exec tipboard runserver