from django.http import HttpResponse, Http404
import datetime
from django.shortcuts import render_to_response
import MySQLdb


def HoursLater(request,offset):
    try:
        offset = int(offset)

    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render_to_response('hours_later.html',{'offset':offset,'then':dt})

def current_time(request):
        now = datetime.datetime.now()
        return render_to_response('current_time.html',{'current_time':now})

def show_users(request):
    db = MySQLdb.connect()
    cursor = db.cursor()
    cursor.execute('SELECT user,host FROM user')
    users = [row for row in cursor.fetchall()]
    db.close()
    return render_to_response('user_list.html',{'users':users})
