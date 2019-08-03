
def format_duration(seconds):
    if seconds == 0:
        return "now"

    time_names = ["year", "day", "hour", "minute", "second"]
    time_seconds = [31536000, 86400, 3600, 60, 1]
    quantities = []

    for i in range(5):
        time = time_seconds[i]
        quantity = seconds // time
        seconds -= quantity * time
        quantities.append(quantity)

    time_string_full = ""
    remaining = sum(q != 0 for q in quantities)

    for i in range(5):
        quantity = quantities[i]
        if quantity != 0:
            time_name = time_names[i]
            time_string = "{} {}{}{}".format(
                str(quantity),
                time_name,
                "s" if quantity > 1 else "",
                ", " if remaining > 2 else " and " if remaining == 2 else ""
            )
            time_string_full += time_string
            remaining -= 1

    return time_string_full
