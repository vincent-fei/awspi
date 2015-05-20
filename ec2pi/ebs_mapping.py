#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import boto.ec2
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType

def ebs_mapping(size=100):
    '''Letter A is used for root device
    Letter B to E are used for Instance Store
    EBS starts from letter F'''
    # 先给个通用配置（非DB）
    # 为了简化，根分区固定为20G，可以用实例存储做swap, 函数参数指定额外EBS磁盘大小,默认100G
    # gp2类型，iops自动为磁盘GB数的3倍
    block_device_map = BlockDeviceMapping()
    xvda = BlockDeviceType(delete_on_termination=True, size=20)
    xvdb = BlockDeviceType(ephemeral_name='ephemeral0')
    xvdf = BlockDeviceType(delete_on_termination=False, size=size, volume_type='gp2')
    #xvdg = BlockDeviceType(delete_on_termination=False, size=100, volume_type='io1', iops=1000)
    block_device_map['/dev/xvda'] = xvda
    block_device_map['/dev/sdb'] = xvdb
    block_device_map['/dev/sdf'] = xvdf
    #block_device_map['/dev/sdg'] = xvdg
    
    return block_device_map
    
if __name__ == '__main__':
    ## then you can use block_device_map in run_instance
    #conn = boto.ec2.connect_to_region(ec2_region)
    #conn.run_instances(
    #    # other arguments
    #    block_device_map=block_device_map,
    #    # other arguments
    #    )
