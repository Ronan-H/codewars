
def format_duration(seconds):
    if seconds == 0:
        return "now"

    times = {
        "year": 31536000,
        "day": 86400,
        "hour": 3600,
        "minute": 60,
        "second": 1
    }
    times_ordered = ["year", "day", "hour", "minute", "second"]
    quantities = []

    for i in range(5):
        time = times[times_ordered[i]]
        quantity = seconds // time
        seconds -= quantity * time
        quantities.append(quantity)

    time_string_full = ""
    remaining = sum(q != 0 for q in quantities)

    for i in range(5):
        quantity = quantities[i]
        if quantity != 0:
            time_name = times_ordered[i]
            time_string = "{} {}{}{}".format(
                str(quantity),
                time_name,
                "s" if quantity > 1 else "",
                ", " if remaining > 2 else " and " if remaining == 2 else ""
            )
            time_string_full += time_string
            remaining -= 1

        if remaining == 0:
            break

    return time_string_full


print(format_duration(12345678))
