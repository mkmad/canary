ps -ef | grep [c]anary- | awk -F ' ' '{print$2}' | xargs kill -9
ps -ef | grep [m]eteor- | awk -F ' ' '{print$2}' | xargs kill -9
