#-*- coding:UTF-8 -*-
import boto
from boto import ec2
from boto.exception import EC2ResponseError
import logging
import MySQLdb

class DBConnector(object):
    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        self.conn = MySQLdb.connect(
                host = host,
                port = port,
                user = user,
                passwd = passwd,
                db = db,
                charset = charset)

    def get_cursor(self):
        return self.conn.cursor()

    def query(self, sql):
        cursor = self.get_cursor()  
        try:
            cursor.execute(sql, None)
            result = cursor.fetchall()  
        except Exception, e:
            logging.error("mysql query error: %s", e)
            return None
        finally:
            cursor.close()
        return result

    def execute(self, sql, param=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, param)
            self.conn.commit()
            affected_row = cursor.rowcount
        except Exception, e:
            logging.error("mysql execute error: %s", e)
            return 0
        finally:
            cursor.close()
        return affected_row

    def executemany(self, sql, params=None):
        cursor = self.get_cursor()
        try:
            cursor.executemany(sql, params)
            self.conn.commit()
            affected_rows = cursor.rowcount
        except Exception, e:
            logging.error("mysql executemany error: %s", e)
            return 0
        finally:
            cursor.close()
        return affected_rows

    def close(self):
        try:
            self.conn.close()
        except:
            pass

    def __del__(self):
        self.close()

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
                ins['instance_id']=instance.id
                ins['name']=instance.tags.get('Name','')
                ins['project']=instance.tags.get('PROJECT','')
                ins['instance_type']=instance.instance_type
                ins['state']=instance.state
                ins['placement']=instance.placement
                ins['private_ip']=instance.private_ip_address
                ins['public_ip']=instance.ip_address
                ins['vpc_id']=instance.vpc_id
                ins['subnet_id']=instance.subnet_id
                ins['image_id']=instance.image_id
                ins['virtualization_type']=instance.virtualization_type
                ins['launch_time']=instance.launch_time
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
                vol['volume_id'] = volume.id
                vol['type'] = volume.type
                vol['size'] = volume.size
                vol['status'] = volume.status
                vol['iops'] = volume.iops
                vol['zone'] = volume.zone
                vol['project'] = volume.tags.get('PROJECT','')
                vol_attr = volume.attach_data
                vol['instance_id'] = vol_attr.instance_id
                vol['snapshot_id'] = volume.snapshot_id
                vol['create_time'] = volume.create_time
                volumes.append(vol)               
        return volumes

def load_data(host,user,passwd,db,port=3306,charset='utf8'):
    # load data into mysql tables
    mysql = DBConnector(host, port, user, passwd, db, charset)
    
    # get all instances
    instances = ec2pi().getAllInstances()
    volumes = ec2pi().getAllVolumes()
    inst_data = []
    for ins in instances:
        InstanceID = ins['instance_id']
        Name = ins['name']
        Project = ins['project']
        InstanceType = ins['instance_type']
        InstanceState = ins['state']
        Placement = ins['placement']
        PrivateIP = ins['private_ip']
        PublicIP = ins['public_ip']
        VpcID = ins['vpc_id']
        SubnetID = ins['subnet_id']
        AmiID = ins['image_id']
        VirtualizationType = ins['virtualization_type']
        LaunchTime = ins['launch_time']
        inst_data.append((InstanceID,Name,Project,InstanceType,
                        InstanceState,Placement,PrivateIP,PublicIP,
                        VpcID,SubnetID,AmiID,VirtualizationType,LaunchTime))
    vol_data = []
    for vol in volumes:
        VolumeID = vol['volume_id']
        VolumeType = vol['type']
        VolumeSize = vol['size']
        AttachState = vol['status']
        VolumeIOPS = vol['iops']
        VolumeZone = vol['zone']
        Project = vol['project']
        InstanceID = vol['instance_id']
        SnapshotID = vol['snapshot_id']
        CreateTime = vol['create_time']
        vol_data.append((VolumeID,VolumeType,VolumeSize,AttachState,VolumeIOPS,
                        VolumeZone,Project,InstanceID,SnapshotID,CreateTime))
        
    load_instance_sql = '''INSERT INTO ec2pi_instances 
                (InstanceID,Name,Project,InstanceType,
                InstanceState,Placement,PrivateIP,PublicIP,
                VpcID,SubnetID,AmiID,VirtualizationType,LaunchTime) 
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
            
    load_volume_sql = '''INSERT INTO ec2pi_volumes 
                            (VolumeID,VolumeType,VolumeSize,AttachState,VolumeIOPS,
                            VolumeZone,Project,InstanceID,SnapshotID,CreateTime)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''           
    
    print mysql.executemany(load_instance_sql, inst_data) 
    print mysql.executemany(load_volume_sql, vol_data) 
    

if __name__ == '__main__':
    # load data into table
    host = '127.0.0.1'
    port = 3306
    user = 'awspi'
    passwd = 'changyou.com'
    db = 'awspi'
    charset = 'utf8'
    load_data(host,user,passwd,db)