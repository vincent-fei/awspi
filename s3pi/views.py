from django.shortcuts import render, render_to_response

# Create your views here.
import boto

def get_object(request):
    bucket_name = 'cypay-filesharing'
    conn = boto.connect_s3()
    b = conn.lookup(bucket_name)
    ob = b.list()
    object_list = []
    for i in ob:
        object_list.append("s3://" + bucket_name + "/" + i.name)
    return render_to_response('listbucket.html',{"object_list":object_list})

def user_data(request):
	values = request.META.items()
	values.sort()
	
	return render_to_response('user_data.html',{'user_data':values})


def s3list(request):
	conn = boto.connect_s3()
	rs = conn.get_all_buckets()
	s3_list = []
	for i in rs:
		_name = "s3://" + i.name
		s3_list.append(_name)
	return  render_to_response('s3list.html',{'s3_list':s3_list})