from django.db import models

# Create your models here.

class Instances(models.Model):
    InstanceID = models.CharField(max_length=10)
    Name = models.CharField(max_length=50)
    Project = models.CharField(max_length=30)
    InstanceType = models.CharField(max_length=12)
    InstanceState = models.CharField(max_length=8)
    Placement = models.CharField(max_length=25)
    PrivateIP = models.CharField(max_length=15)
    PublicIP = models.CharField(max_length=15)
    VpcID = models.CharField(max_length=12)
    SubnetID = models.CharField(max_length=15)
    AmiID = models.CharField(max_length=12)
    VirtualizationType =  models.CharField(max_length=24)
    LaunchTime = models.CharField(max_length=24)
    def __unicode__(self):
        return self.InstanceID

class Volumes(models.Model):
    VolumeID = models.CharField(max_length=12)
    VolumeType = models.CharField(max_length=8)
    VolumeSize = models.CharField(max_length=5)
    AttachState = models.CharField(max_length=5)
    VolumeIOPS = models.CharField(max_length=6)
    VolumeZone = models.CharField(max_length=18)
    Project = models.CharField(max_length=30)
    InstanceID = models.CharField(max_length=10)
    SnapshotID = models.CharField(max_length=10)
    CreateTime = models.CharField(max_length=24)
    def __unicode__(self):
        return self.VolumeID
