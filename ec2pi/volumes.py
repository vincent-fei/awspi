#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from boto import ec2
from boto.exception import EC2ResponseError
import boto
from pymongo import MongoClient

class MongoTool:
    db=None
    def __init__(self,host,port):
        client = MongoClient(r"mongodb://%s:%s" %(mongo-host,port))
        self.db=client.asetinfo

    #插入或者更新aws volumes记录，如果已经存在则更新，如果没有则插入
    def insertOrUpdateVolumes(self,volumes):
        results={}
        results['error_count']=0
        results['modified_count']=0
        results['total_record']=len(volumes)
        for volume in volumes:
            try:
                rs=self.db.volumes.update_one(
                    {'_id':volume['_id']},
                    {'$set': volume},
                    upsert=True
                )
                results['modified_count']=results['modified_count']+rs.modified_count
            except :
                results['error_count']=results['error_count']+1

        return results

class AwsTool:
    #获取某个AWS账号下所有region的所有volumes
    def getAllVolumes(self,aws_access_key_id,aws_secret_access_key):
        try:
            #尝试Key的有效性并判断属于大陆区还是海外区，并获得相应的regions列表
            conn = ec2.connect_to_region('ap-southeast-1',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            regions = conn.get_all_regions()
            accountid = boto.connect_iam(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key).get_user().arn.split(':')[4]
        except EC2ResponseError as e:
            print e
            
        volumes=[]            
        for region in regions:
            print "connect to region", region
            conn = ec2.connect_to_region(region.name,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
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

if __name__ == '__main__':
    #get volumes and load into mongodb
    volumes = AwsTool().getAllVolumes()
    mongoTool = MongoTool(mongo-host,port)
    mongoTool.insertOrUpdateVolumes(volumes)
