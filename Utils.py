def seconds_to_minsec(total_seconds):
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    minute_second = "{:02d}:{:02d}".format(minutes, seconds)

    return minute_second

def coordinates_to_meters(coord_length):
    return coord_length*111320

if __name__=="__main__":
    print (seconds_to_minsec(1880))