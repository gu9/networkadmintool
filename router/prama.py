import re,os
import paramiko
import time
import sys
from router.models import Routerpara,Routerprotocol



def ssh_commands(ip,uname,password):

        router={}
        s=paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(ip,username=uname,password=password)
        conn=s.invoke_shell()
        conn.send("terminal length 0 \n")
        cmds='''show version | include (, Version|uptime is|bytes of memory|Hz)&\
         show processes cpu | include CPU utilization&\
         show ip protocols | include Routing Protocol&\
         show memory statistics'''
        commands=cmds.split("&")

        for line in commands:
            conn.send(line +'\n')
            time.sleep(1)
        out_put=conn.recv(65535)
        if re.search(r"% Invalid input detected at",out_put):
            print 'none is thre'
        else:
            pass
        s.close()

        get_hostname=re.search(r"(.+) uptime is",out_put)
        hname=get_hostname.group(1)
        

        vendor_name=re.search(r"(.+?) (.+?) (.+) bytes of memory",out_put)
        vname=vendor_name.group(1)
        

        get_model=re.search(r"(.+?) (.+?) (.+) bytes of memory",out_put)
        model=get_model.group(2)
     
        image_name = re.search(r" \((.+)\), Version", out_put)
        image = image_name.group(1)
        

        get_os = re.search(r"\), Version (.+),", out_put)
        os = get_os.group(1)

        #print"os",os
        cpu_util = re.search(r"CPU utilization for five seconds: (.+) five minutes: (.+?)%", out_put)
        cpuper5min = cpu_util.group(2)
    
        if re.search(r"(.+?)at (.+?)MHz(.+)\n", out_put) == None:
            cpuspeed = "unknown"
        else:
            cpuspeed = re.search(r"(.+?)at (.+?)MHz(.+)\n", out_put).group(2)
        print"cpu_speed", cpuspeed+'Mhz'
        io_memory = re.search(r"      I/O(.+)\n", out_put)
        usedmem = io_memory.group(1)
        memory_total_io_mem = usedmem.split('   ')[2].strip()
        memory_used_io = usedmem.split('   ')[3].strip()
        routing_run = re.findall(r"Routing Protocol is \"(.+)\"\r\n",out_put)
        outer=[]
        
        for index in routing_run:
            outer.append(index)
        outer_pro=",".join(outer)
        try:
            heck=Routerprotocol.objects.get(hostip=ip)
            if not heck :
                Routerprotocol.objects.filter(hostip=ip).update(hostip=ip,outer_protocols=outer_pro)
        except Routerprotocol.DoesNotExist:
            h1=Routerprotocol(hostip=ip,outer_protocols=outer_pro)
            h1.save()
        except Routerprotocol.MultipleObjectsReturned:
            Routerprotocol.objects.filter(hostip=ip).update(hostip=ip,outer_protocols=outer_pro)
            
        router[hname]=[vname,model,image,os,cpuper5min,cpuspeed,memory_total_io_mem,memory_used_io]
        try:
            check=Routerpara.objects.get(host_name=hname)
            if not check :
                for key,value in router.iteritems():
                    Routerpara.objects.filter(host_name=hname).update(host_name=key,vendor_name=value[0], model_name=value[1],image_name=value[2],version_name=value[3],cpu_usage=value[4],cpu_speed=value[5],mem_tot=value[6],mem_used=value[7])   
        except Routerpara.DoesNotExist:
                for key,value in router.iteritems():
                    p1=Routerpara(host_name=key,vendor_name=value[0], model_name=value[1],image_name=value[2],version_name=value[3],cpu_usage=value[4],cpu_speed=value[5],mem_tot=value[6],mem_used=value[7])   
                    p1.save()
        except Routerpara.MultipleObjectsReturned:
                for key,value in router.iteritems():     
                    Routerpara.objects.filter(host_name=hname).update(host_name=key,vendor_name=value[0], model_name=value[1],image_name=value[2],version_name=value[3],cpu_usage=value[4],cpu_speed=value[5],mem_tot=value[6],mem_used=value[7])   
        

