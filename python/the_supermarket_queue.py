
def queue_time(customers, n):
    tills = [0] * n
    time = 0

    while len(customers) > 0 or any(c != 0 for c in tills):
        t = 0

        while t < len(tills) and len(customers) > 0:
            if tills[t] == 0:
                tills[t] = customers[0]
                del customers[0]
            t += 1

        min_cust = min(val for val in tills if val != 0)

        for t in range(len(tills)):
            tills[t] = max(tills[t] - min_cust, 0)

        time += min_cust

    return time
