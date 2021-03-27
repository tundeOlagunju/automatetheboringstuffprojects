from datetime import datetime

def curr_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')