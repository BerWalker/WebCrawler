import time
import threading

def make_web_request():
    print("Making web request...")
    time.sleep(3)
    print("Finished web request")

# Creating multiple threads for web requests
thread_1 = threading.Thread(target=make_web_request)
thread_1.start()

thread_2 = threading.Thread(target=make_web_request)
thread_2.start()

thread_3 = threading.Thread(target=make_web_request)
thread_3.start()
