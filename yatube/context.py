import datetime as dt

#дата в контекст процессоре
def year(request):
    date = dt.datetime.now().year
    return {"year": date}