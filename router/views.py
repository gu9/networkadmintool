from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from router.RouterInfoForm import RouterInfo,ip_lookup
from django.template import RequestContext
from router.models import RouterAd, Routerpara, Routervrf_lookup,Routerprotocol
from django.contrib import auth
from router.ipcheck import ip_valid
from router.is_ip_valid import ipvalid
import prama 
import sys
import os
import subprocess
from router.models import Routerint,Routervrfs
from router.allextarct import Main
def RouterRegisteration(request):
    if request.method =='POST':
        NewForm=RouterInfo(request.POST)
        if NewForm.is_valid():
            hname=NewForm.cleaned_data['host_name']
            hip=NewForm.cleaned_data['host_ip']
            pword=NewForm.cleaned_data['password']
            uname=NewForm.cleaned_data['user_name']
            result=ipvalid(hip)
            if result:
                router_info=RouterAd(host_name=hname,host_ip=hip,user_name=uname,password=pword)
                router_info.save()
                return HttpResponseRedirect('/router/index/') 
            else:
                return render(request,"err_form.html",{'ipinvalid':1})
    else:
        NewForm=RouterInfo()
        context={'form':NewForm}
        return render_to_response('rtr_add.html',context,context_instance=RequestContext(request))

# Create your views here.
def allhostrequest(request):
    context={
             'allhosts':RouterAd.objects.all()
             }
    if request.method=="POST":
        h1=request.POST.getlist('my_options')
        try:
        
            obj=RouterAd.objects.get(host_name= h1[0])
            request.session['ip']=obj.host_ip
            request.session['host']=obj.host_name
            request.session['password']=obj.password
            #result=ssh_conn(str(obj.host_ip),"gopi","cisco")
            result=Main(obj.host_ip,obj.host_name)
            if result:
                request.session.update({
                                        'ip':obj.host_ip,
                                        'host':obj.host_name,
                                        'password':obj.password})
                
                
                return render(request,"dashbord.html",{'host_session':obj.host_name,'ip_addr':obj.host_ip})
            else:
                return render(request,"err_form.html",{'allhostrequest':1})
            
        except RouterAd.DoesNotExist:
            pass                 
    return render_to_response('allhost.html',context,context_instance=RequestContext(request))
def logout_view(request):
    del request.session['ip']
    del request.session['host']
    del request.session['password']
    Routerint.objects.all().delete()
    Routervrfs.objects.all().delete()
    Routervrf_lookup.objects.all().delete()
    Routerpara.objects.all().delete()
    Routerprotocol.objects.all().delete()
    return HttpResponseRedirect('/router/index/')

def allvrfrequest(request):
    ip_address=request.session['ip']
    host=request.session['host']
    password=request.session['password']
    context={'allvrfs':Routervrfs.objects.filter(hostip=ip_address),'ip_addr':ip_address}
    if request.method=="POST":
        h1=request.POST.getlist('my_options')
        result=Routervrf_lookup.objects.filter(customer_name=h1[0])
        return render(request,"vrf_spec.html",{'vrfs':result,'ip_addr':ip_address,'cust':h1[0]})
    return render_to_response('vrfdrop_menu.html',context,context_instance=RequestContext(request))
    
    
    
def vrf_show(request):
    if request.session.has_key("ip") and request.session.has_key("host") and request.session.has_key("password"):
        router_ip=request.session['ip']
        router_name=request.session['host']
        router_password=request.session['password']
        result=Routervrfs.objects.filter(hostip=router_ip)
        context={'ip_addr':router_ip,
                 'router':result}
        return render_to_response('vrf_show.html',context,context_instance=RequestContext(request))
    else:
        return render(request,'err.html',{'none_check':1})
        
        
def show_interface_view(request):
    if request.session.has_key("ip") and request.session.has_key("host") and request.session.has_key("password"):
        router_ip=request.session['ip']
        router_name=request.session['host']
        router_password=request.session['password']
        result=Routerint.objects.filter(hostip=router_ip)
        return render(request,"interface.html",{'ip_addr':router_ip,'router':result})
    else:
        return render(request,'err.html',{'none_check':1})
        
    
def performance_view(request):
    if  request.session.has_key("ip") and request.session.has_key("host") and request.session.has_key("password"):
        router_ip=request.session['ip']
        router_name=request.session['host']
        router_password=request.session['password']
        result=Routerpara.objects.filter(host_name=router_name)
        return render(request,"demo.html",{'ip_addr':router_ip,'router':result})
    else:
        return render(request,'err.html',{'none_check':1})
        
def ip_lookup_view(request):
    if request.session.has_key("ip") and request.session.has_key("host") and request.session.has_key("password"):
        if request.method=="POST":
            selected_vrf=request.POST.getlist('my_options')
            ip=request.POST.get('ip_field')
            mask=request.POST.get('mask_field')
            print selected_vrf[0]
            if ip==None or mask==None:
                return render(request,'err.html',{'fieldempty':1})
            else:
                check=ip_valid(str(ip),str(mask))
                if check:
                    result=Routervrf_lookup.objects.filter(customer_name=selected_vrf[0])
                    for item in result:
                        if  item.network==check:
                            
                            return render(request,"ip_found.html",{'check':ip,'ip_addr':request.session['ip'],'vrf':selected_vrf[0],'allpara':item})
                    return  render(request,"ip_found.html",{'error':ip,'ip_addr':request.session['ip'],'vrf':selected_vrf[0]})
                else:
                    return render(request,'err.html',{'none_check':1})
                
        else:
            NewForm=ip_lookup()
            ip_address=request.session['ip']
            context={'form':NewForm,'allvrfs':Routervrfs.objects.filter(hostip=ip_address),'ip_addr':ip_address}
            return render_to_response('ip_look.html',context,context_instance=RequestContext(request))
    else:
        return render(request,'err.html',{'loginfirst':1})      
            
        
def protocol_view(request):
        if request.session.has_key("ip") and request.session.has_key("host") and request.session.has_key("password"):
            result= Routerprotocol.objects.filter(hostip=request.session['ip'])
            for item in result:
                context={'data':item,'ip_addr':request.session['ip']}
                return render(request,"show_pro.html",context)
                
            return render(request,'err.html',{'loginfirst':1}) 
        else:
            
            return render(request,'err.html',{'loginfirst':1})  
    
    
    
    
    