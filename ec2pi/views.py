#-*- coding:UTF-8 -*-
from django.shortcuts import render, render_to_response

# Create your views here.
import boto
from boto import ec2

class ec2pi:
    def getAllInstances(self):
        try:
            #尝试Key的有效性并判断属于大陆区还是海外区，并获得相应的regions列表
            conn = ec2.connect_to_region('ap-southeast-1')
            regions = conn.get_all_regions()            
            accountid = boto.connect_iam().get_user().arn.split(':')[4]
        except EC2ResponseError as e:
            print e
            
        instances=[]
        for region in regions:
            conn=ec2.connect_to_region(region.name)
            for instance in conn.get_only_instances():
                ins={}
                ins['_id']=instance.id
                ins['accountid']=accountid
                ins['region']=region.name
                #ins['public_dns_name']=instance.public_dns_name
                #ins['private_dns_name']=instance.private_dns_name
                ins['state']=instance.state
                ins['key_name']=instance.key_name
                ins['instance_type']=instance.instance_type
                ins['launch_time']=instance.launch_time
                ins['image_id']=instance.image_id
                ins['placement']=instance.placement                
                #ins['kernel']=instance.kernel                
                ins['architecture']=instance.architecture
                ins['hypervisor']=instance.hypervisor
                ins['virtualization_type']=instance.virtualization_type
                ins['monitored']=instance.monitored                               
                ins['subnet_id']=instance.subnet_id
                ins['vpc_id']=instance.vpc_id
                ins['private_ip_address']=instance.private_ip_address
                ins['ip_address']=instance.ip_address
                ins['platform']=instance.platform
                ins['root_device_name']=instance.root_device_name
                ins['root_device_type']=instance.root_device_type

                #get tags
                ins['name']=instance.tags['Name']
                instances.append(ins)
        return instances

    def getAllVolumes(self):
        try:
            #尝试Key的有效性并判断属于大陆区还是海外区，并获得相应的regions列表
            conn = ec2.connect_to_region('ap-southeast-1')
            regions = conn.get_all_regions()
            accountid = boto.connect_iam().get_user().arn.split(':')[4]
        except EC2ResponseError as e:
            print e
            
        volumes=[]            
        for region in regions:
            #print "connect to region", region
            conn = ec2.connect_to_region(region.name)
            for volume in conn.get_all_volumes():                
                vol={}               
                vol['_id'] = volume.id
                vol['status'] = volume.status
                vol['attachment_state'] = volume.attachment_state()
                vol['create_time'] = volume.create_time
                vol['encrypted'] = volume.encrypted
                vol['region'] = volume.region.name
                vol['zone'] = volume.zone
                vol['size'] = volume.size
                vol['type'] = volume.type
                vol['iops'] = volume.iops
                vol['tags'] = volume.tags
                vol['snapshot_id'] = volume.snapshot_id               
                vol['accountid'] = accountid
                
                attachment = {}
                vol_attr = volume.attach_data
                attachment['_id'] = vol_attr.id
                attachment['instance_id'] = vol_attr.instance_id              
                attachment['attach_time'] = vol_attr.attach_time
                #attachment['deleteOnTermination'] = vol_attr.deleteOnTermination
                attachment['device'] = vol_attr.device
                
                vol['attach_data'] = attachment               
                volumes.append(vol)               
        return volumes

def ListInstances(request):
	# get all instances
	instances = ec2pi().getAllInstances()
	return render_to_response('listinstance.html',{'instances':instances})
	
def ListVolumes(request):
	# get all volumes
	volumes = ec2pi().getAllVolumes()
	return render_to_response('listvolume.html',{'volumes':volumes})