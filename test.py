from datetime import datetime, time

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

# Original test case from OP
if is_time_between(time(12,40), time(16,30)):
    print("now")
else:
    print("not now")

# Test case when range crosses midnight
print(is_time_between(time(22,0), time(4,00)))

if is_time_between(time(22,40), time(06,30)):
    print("now")
else:
    print("not now")
