import paramiko
import re
import socket
import sys
import datetime
import time
from router.models import Routerint,Routervrfs,Routervrf_lookup
import prama
from multiprocessing.pool import ThreadPool


class ssh_conn_th():
    def __init__(self,ip,u,p,cmds):
        self.ip=ip
        self.user_name=u
        self.password=p
        self.cmds=cmds
        #self.out1=None
    def run_fun(self):
        try:
            self.session=paramiko.SSHClient()
            self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.session.connect(self.ip,username=self.user_name,password=self.password)
            self.stdin,self.stdout,self.stderr=self.session.exec_command(self.cmds)
            out1=self.stdout.readlines()
            self.stdin.flush()
            self.session.close()
            return out1
        except paramiko.ssh_exception.AuthenticationException:
            return None
        except paramiko.ssh_exception.BadAuthenticationType:
            return None
        except paramiko.ssh_exception.BadHostKeyException:
            return None
        except paramiko.ssh_exception.ChannelException:
            return None
        except paramiko.ssh_exception.PartialAuthentication:
            return None
        except paramiko.ssh_exception.PasswordRequiredException:
            return None
        except paramiko.ssh_exception.ProxyCommandFailure:
            return None
        except paramiko.ssh_exception.SSHException:
            return None
        except socket.error:
            return None

def extract_interface(output,ip_address,host):
    router={}
    for i in output:
        text = str(i.encode('ascii', 'replace'))
        match = re.findall(r'[0-9]+(?:\.[0-9]+){3}',text)

        if match:
            interface_name=text.split()[0]
            ipadd=text.split()[1]
            stat=text.split()[4]
            prot=text.split()[5]
            method=text.split()[3]
            sqltime=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            router[interface_name]=[ipadd,stat,prot,method,sqltime]
        else:
             list_a=text.split()
             if not list_a :
                 continue
             elif "Interface" in list_a:
                 continue
             else:
                 interface_name=text.split()[0]
                 ipadd=text.split()[1]+host
                 
                 stat=text.split()[4]
                 prot=text.split()[5]
                 method=text.split()[3]
                 sqltime=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                 router[interface_name]=[ipadd,stat,prot,method,sqltime]
    try:
        check=Routerint.objects.get(hostip=ip_address)
        if not check :
            for key,value in router.iteritems():
                Routerint.objects.filter(ip_addr=value[0]).update(hostip=ip_address,interface_name=key,ip_addr=value[0], admin_up=value[1],protocol_up=value[2],t_stamp=value[4])
    except Routerint.DoesNotExist:
        for key,value in router.iteritems():
                p1=Routerint(hostip=ip_address,interface_name=key,ip_addr=value[0], admin_up=value[1],protocol_up=value[2],t_stamp=value[4])
                p1.save()
    except Routerint.MultipleObjectsReturned:
                for key,value in router.iteritems():
                    Routerint.objects.filter(ip_addr=value[0]).update(hostip=ip_address,interface_name=key,ip_addr=value[0], admin_up=value[1],protocol_up=value[2],t_stamp=value[4])


def extract_vrfs(output,ip_address):
    router={}
    for i in output:
        text = str(i.encode('ascii', 'replace'))
        match = re.findall(r"([A-Za-z]*)([0-9]*)/([0-9]*)", text)
        if match:
            vrf_name=text.split()[0]
            vrf_RD=text.split()[1]
            vrf_int=text.split()[2]
            router[vrf_name]=[vrf_RD,vrf_int]
    try:
        check=Routervrfs.objects.get(hostip=ip_address)
        if not check :
            for key,value in router.iteritems():
                Routervrfs.objects.filter(vrf_name=key).update(hostip=ip_address,vrf_name=key, vrf_RD=value[0],vrf_int=value[1])
    
    except Routervrfs.DoesNotExist:
        for key,value in router.iteritems():
                p1=Routervrfs(hostip=ip_address,vrf_name=key, vrf_RD=value[0],vrf_int=value[1])
                p1.save()
    except Routervrfs.MultipleObjectsReturned:
            for key,value in router.iteritems():
                Routervrfs.objects.filter(vrf_name=key).update(hostip=ip_address,vrf_name=key, vrf_RD=value[0],vrf_int=value[1])
                
    #print router

def vrf_routes_specific(out1,ip_address):

    flag=0
    no_of_subnets=0
    result={}
    sqltime=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    for i in out1:
        text=str(i.encode('ascii','replace'))
        if flag==0:
				match=re.search("Routing Table:", text)
				if match:
					customer=text.split()[2]
					result[customer]=[]
					counter=0
					flag=1
        elif (flag==1):
				match=re.search("Routing Table:", text)
				if match:
					customer=text.split()[2]
					result[customer]=[]
					counter=0
					flag=1
				else:
					if re.search("is subnetted",text):
						match2=re.search('(?<=/)(.*)', text)
						netmask=match2.group(0).split()[0]
						match2=re.search('(?<=,)(.*)', text)
						no_of_subnets=int(match2.group(0).split()[0])
						continue
					if no_of_subnets>0:
						if re.search("is directly connected",text):
							protocol1=text.split()[0]
							if protocol1=='C':
								protocol1="Connected"
							network1=text.split()[1]+"/"+netmask
							result[customer].append([network1,protocol1,'', sqltime])
							counter=counter+1
						elif (text[0]=='B' or text[0]=='O') :
							protocol1=text.split()[0]
							if protocol1=='B':
								protocol1="BGP"
							elif protocol1=='O':
								protocol1="OSPF"
							network1=text.split()[1]+"/"+netmask
							match2=re.search('(?<=via)(.*)', text)
							nexthop=(match2.group(0).split(',')[0]).split()[0]
							result[customer].append([network1,protocol1,nexthop, sqltime])
						no_of_subnets=no_of_subnets-1
					else:
						if re.search("is directly connected",text):
							protocol1=text.split()[0]
							if protocol1=='C':
								protocol1="Connected"
							network1=text.split()[1]
							result[customer].append([network1,protocol1,'', sqltime])
							counter=counter+1
						if ((text[0]=='B') or (text[0]=='O')):
							protocol1=text.split()[0]
							if protocol1=='B':
								protocol1="BGP"
							elif protocol1=='O':
								protocol1="OSPF"
							network1=text.split()[1]
							match2=re.search('(?<=via)(.*)', text)
							nexthop=(match2.group(0).split(',')[0]).split()[0]
							result[customer].append([network1,protocol1,nexthop, sqltime])
							counter=counter+1
    if result:
    
        try:
            check=Routervrf_lookup.objects.get(router_id=ip_address)
            if not check :
                for i in range(len(result.keys())):
                    for j in range(len(result.values()[i])):
                        
                        
                        if result.values()[i][j][1]=='Connected':
                            location=result.keys()[i]
                        Routervrf_lookup.objects.filter(network=result.values()[i][j][0]).update(router_id=ip_address,customer_name=result.keys()[i],network=result.values()[i][j][0],protocol=result.values()[i][j][1],nexthop=result.values()[i][j][2],timestamp=result.values()[i][j][3])
        except Routervrf_lookup.DoesNotExist:
            for i in range(len(result.keys())):
                    for j in range(len(result.values()[i])):
                        if result.values()[i][j][1]=='Connected':
                            location=result.keys()[i]
                        p1=Routervrf_lookup(router_id=ip_address,customer_name=result.keys()[i],network=result.values()[i][j][0],protocol=result.values()[i][j][1],nexthop=result.values()[i][j][2],timestamp=result.values()[i][j][3])
                        p1.save()
        except Routervrf_lookup.MultipleObjectsReturned:
            for i in range(len(result.keys())):
                    for j in range(len(result.values()[i])):
                        if result.values()[i][j][1]=='Connected':
                            location=result.keys()[i]
                        vrf_new=Routervrf_lookup.objects.filter(network=result.values()[i][j][0]).update(router_id=ip_address,customer_name=result.keys()[i],network=result.values()[i][j][0],protocol=result.values()[i][j][1],nexthop=result.values()[i][j][2],timestamp=result.values()[i][j][3])
            
            
def Main(ip_address,host):
    obj1=ssh_conn_th(ip_address,"gopi","cisco","show ip int br")
    ex_int=obj1.run_fun()
    if ex_int:
        extract_interface(ex_int,ip_address,host)
    else:
        return None
    #****************************Show ip vrf***************
    obj2=ssh_conn_th(ip_address,"gopi","cisco","show ip vrf")
    ex_vrfs=obj2.run_fun()
    if ex_vrfs:
        extract_vrfs(ex_vrfs,ip_address)
    else:
        return None
    #**************CPU SSH code*******************
    p=ThreadPool(processes=1)
    get_result=p.apply_async(prama.ssh_commands,(ip_address,"gopi","cisco",))
    #*****************************Show ip vrf +(vrf name)**********
    obj3=ssh_conn_th(ip_address,"gopi","cisco","show ip route vrf *")
    ext_vrf_routes=obj3.run_fun()
    if ex_vrfs:
        vrf_routes_specific(ext_vrf_routes,ip_address)
    else:
        return None
    
    return True
    