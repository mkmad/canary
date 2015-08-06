ps -ef | grep [r]edis-server | awk -F ' ' '{print$2}' | xargs kill -9

# run redis
exec redis-server > /dev/null 2>&1 &

# run the UI
exec tipboard runserver > /dev/null 2>&1 &

# run the data collector to push to the UI
exec python data_collector.py
