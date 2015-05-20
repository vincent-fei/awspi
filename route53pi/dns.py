#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wangfei 2014-12-26

import boto.route53
import os

def check_domain_name(domain_name):
    '''check if this domain name is legal or not
    route53 domain name must ends with dot
    if not, I will add a single dot for you
    '''   
    if input.endswith('.'):
        hosted_zone_name = domain_name
    else:
        hosted_zone_name = domain_name + '.'
    return hosted_zone_name
        
def add_record_to_zone(domain_name,type,sub_domain,value,ttl=300):
    ## check domain_name ends with dot or not
    hosted_zone_name = check_domain_name(domain_name)
    ## route53 has no region, so just randomly give it a region for conection endpoint    
    conn = boto.route53.connect_to_region('ap-southeast-1')
    zone = conn.get_zone(hosted_zone_name)
    record_type = type
    record_set = sub_domain + '.' + hosted_zone_name
    record_value = value
    record_ttl = int(ttl)
    if zone.find_records(record_set,record_type):
        print "ERROR, record set already exists"
    else:
        zone.add_record(record_type, record_set, record_value,record_ttl)
        print "record set added successfully"
        print record_set,record_value
    
def delete_record_from_zone(domain_name,type,sub_domain):
    ## check input ends with dot or not
    hosted_zone_name = check_domain_name(domain_name)
    ## route53 has no region, so just randomly give it a region for conection endpoint        
    conn = boto.route53.connect_to_region('ap-southeast-1')
    zone = conn.get_zone(hosted_zone_name)
    record_type = type
    record_set = sub_domain + '.' + hosted_zone_name
    record_find_result = zone.find_records(record_set,record_type)
    if not record_find_result:
        print "ERROR, record set does NOT exists"
    else:
        zone.delete_record(record_find_result)
        print "record set %s deleted" % record_set

def export_zone_to_file(domain_name,type,sub_domain):
    '''
    export hosted zone to text file
    you can use the exported file to load into route53 again later in any aws account
    '''
    ## check input ends with dot or not
    ## zone name have to be domain name ends with dot
    hosted_zone_name = check_domain_name(domain_name)
    # make connection to route53   
    conn = boto.route53.connect_to_region('ap-southeast-1')
    zone = conn.get_zone(hosted_zone_name)
    records = zone.get_records()
    # write output to file
    output_fle = os.sys.path[0] + os.sep + hosted_zone_name + 'records.txt'
    f = open(output_fle,'w')
    for record in records:
        output = "%s\tIN\t%s\t%s\t%s" % (record.name,record.type,record.ttl, ",".join(record.resource_records))
        f.writelines(str(output) + "\n")
    f.close()


if __name__ == '__main__':
    # useage demos
    #export_zone_to_file('imbusy.me')
    #add_record_to_zone('cypay.internal','A','www','10.0.1.175')
    #add_record_to_zone('cypay.internal','CNAME','web','www.cypay.internal')
    #delete_record_from_zone('cypay.internal','A','www')
