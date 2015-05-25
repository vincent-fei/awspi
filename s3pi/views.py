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
