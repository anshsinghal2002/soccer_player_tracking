def seconds_to_minsec(total_seconds):
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    minute_second = "{:02d}:{:02d}".format(minutes, seconds)

    return minute_second