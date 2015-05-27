#-*- coding:UTF-8 -*-
from django.shortcuts import render, render_to_response
import MySQLdb

# Create your views here.

def ListInstances(request):
	# get all instances
	# 连接数据库　
	try:
	    conn = MySQLdb.connect(host='127.0.0.1',user='awspi',passwd='changyou.com',db='awspi')
	except Exception, e:
	    print e
	    sys.exit()
 	# 获取cursor对象来进行操作
 	cursor = conn.cursor()
 
	#查询出数据
	sql = "select * from ec2pi_instances;"
	cursor.execute(sql)
	instances = cursor.fetchall()	 
	cursor.close()
	conn.close()
	return render_to_response('listinstance.html',{'instances':instances})

def ListVolumes(request):
	# get all volumes
	# 连接数据库　
	try:
	    conn = MySQLdb.connect(host='127.0.0.1',user='awspi',passwd='changyou.com',db='awspi')
	except Exception, e:
	    print e
	    sys.exit()
 	# 获取cursor对象来进行操作
 	cursor = conn.cursor()
 
	#查询出数据
	sql = "select * from ec2pi_volumes;"
	cursor.execute(sql)
	volumes = cursor.fetchall()	 
	cursor.close()
	conn.close()	
	return render_to_response('listvolume.html',{'volumes':volumes})