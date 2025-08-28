#!/bin/bash
# 启动Nginx服务（serving静态资源）
nginx -c /app/nginx.conf &
# 启动保活脚本
python keep_alive.py &
# 等待进程，避免服务退出
wait -n
exit $?