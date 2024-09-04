nohup python chat_main_asyncio.py >logs/log/chat_main_asyncio.txt 2>&1 & echo $! > logs/pid/chat_main_asyncio.pid

# kill -9 $(cat logs/pid/run{1..8}.pid)