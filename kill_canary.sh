ps -ef | grep [c]anary- | awk -F ' ' '{print$2}' | xargs kill -9
