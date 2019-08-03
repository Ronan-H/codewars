
def format_duration(seconds):
    times = {"year": 31536000,
             "day": 86400,
             "hour": 3600,
             "minute": 60,
             "seconds": 1}
    time_names = ["year", "day", "hour", "minute", "second"]
    quantities = []

    for time_name, time in times.items():
        quantity = seconds // time
        seconds -= quantity * time
        quantities.append(quantity)

    print(quantities)


print(format_duration(3662))
