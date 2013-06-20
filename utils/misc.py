import pdb

def time_ago(timestamp):
    """
    Returns a human readable time ago string
    
    Input
    ----
        timestamp - A datatetime object
        
    Output
    ------
        a strings with the time in the for of "xx minutes ago"
    
    """
    
    from datetime import datetime as dt
    
    now = dt.utcnow()
    age = now-timestamp.replace(tzinfo=None)
    
    if age.seconds < 60*60:
        m = age.seconds/60
        if m == 1:
            txt =  "%s minute ago"
        else:
             txt = "%s minutes ago"
        out = txt %(m)

    if age.seconds < 24*60*60:
        h = age.seconds/60/60
        if h == 1:
            txt = "%s hour ago"
        else:
            txt = "%s hours ago"
        out = txt %(h)

    if age.days >= 1:
        if age.days == 1:
            txt = "%s day and %s hours ago"
        else: 
            txt = "%s days and %s hours ago"
        out = txt %(age.days, age.seconds/60/60)

    if age.days >= 7:
        out = "%s days ago" %(age.days)

    return out