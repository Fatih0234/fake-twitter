def how_long_since(seconds):
    
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)
    years, months = divmod(months, 12)
    print(years, months, days, hours, minutes, seconds)
    
    if years > 0:
        return "%dy" % years
    elif months > 0:
        return "%dm" % months
    elif days > 0:
        return "%dd" % days
    elif hours > 0:
        return "%dh" % hours
    elif minutes > 0:
        return "%dm" % minutes
    else:
        return "Just now!"
    
print(how_long_since(60))