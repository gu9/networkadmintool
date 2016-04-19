from django.db import models

class RouterAd(models.Model):
    host_name = models.CharField(max_length=32)
    host_ip = models.CharField(max_length=32)
    user_name=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    
    
class Routerint(models.Model):
    hostip = models.CharField(max_length=32)
    interface_name=models.CharField(max_length=32)
    ip_addr=models.CharField(max_length=32)
    admin_up=models.CharField(max_length=30)
    protocol_up=models.CharField(max_length=20)
    t_stamp = models.DateTimeField()
   
class Routerprotocol(models.Model):
    hostip=models.CharField(max_length=32)
    outer_protocols= models.CharField(max_length=200)
    
class Routerpara(models.Model):
    host_name = models.CharField(max_length=32)
    vendor_name= models.CharField(max_length=32)
    model_name=models.CharField(max_length=32)
    image_name=models.CharField(max_length=32)
    version_name = models.CharField(max_length=32)
    cpu_usage = models.CharField(max_length=32)
    cpu_speed=models.CharField(max_length=32)
    mem_tot=models.CharField(max_length=32)
    mem_used=models.CharField(max_length=32)
    
class Routervrfs(models.Model):
    hostip = models.CharField(max_length=32)
    vrf_name = models.CharField(max_length=32)
    vrf_RD = models.CharField(max_length=32)
    vrf_int=models.CharField(max_length=32)
    
class Routervrf_lookup(models.Model):
    router_id = models.CharField(max_length=50)
    customer_name= models.CharField(max_length=50)
    network=models.CharField(max_length=50)
    protocol=models.CharField(max_length=50)
    nexthop = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    
    
    

   
    