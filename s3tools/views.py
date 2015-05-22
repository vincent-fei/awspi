from django.shortcuts import render
from django.shortcuts import render_to_response

from boto.s3.connection import S3Connection

# Create your views here.
from django.http import HttpResponse, Http404

def user_data(request):
	values = request.META.items()
	values.sort()
	
	return render_to_response('user_data.html',{'user_data':values})


def s3list(request):
	conn = S3Connection()
	rs = conn.get_all_buckets()
	s3_list = []
	for i in rs:
		_name = "s3://" + i.name
		s3_list.append(_name)
	return  render_to_response('s3list.html',{'s3_list':s3_list})