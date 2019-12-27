#coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render
import requests,json
from django.shortcuts import redirect
from django.conf import settings
from datetime import datetime
import dateutil.parser

def hello(request):
    return HttpResponse("Hello world!")

def index(request):
    context ={}
    if not (request.session.has_key('username') and request.session['username'] !=''):
       return redirect('login.html')
    context['username'] = request.session['username']
    #context['tokenid'] = request.session['tokenid']
    return render(request,'index.html',context)    



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == " ":
            return HttpResponse('请输入用户名！')
        if password == " ":
            return HttpResponse('请输入密码！') 

        data=json.dumps({
           "auth": {               
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": username,
                            "domain": {
                                "name": "default"
                            },
                            "password": password
                        }
                    }
                },
            }
        })       
        #info = requests.post('http://192.168.119.128:5000/v3/auth/tokens',data)
        info = requests.post(settings.KEYSTORN+'/v3/auth/tokens',data)
        head = info.headers
        x = requests.structures.CaseInsensitiveDict(head)
        js = dict(x)
        info = info.json()
        #print info
        if info.has_key('token'):
            request.session['tooken'] = info
            request.session['userid'] = info['token']['user']['id']
            request.session['username'] = info['token']['user']['name']
            request.session['tokenid'] = js['X-Subject-Token']
            return redirect('index.html')
            return HttpResponse('登录成功！')
        else:
            return HttpResponse('用户名或密码错误！')
        
    context = {}
    return render(request,'login.html',context) 
def loginout(request):
    if request.method =='POST':
        auth.loginout(request)
        return HttpResponseRedirect('login') 

def image(request):
    context={}
    if not (request.session.has_key('username') and request.session['username'] !=''):
       return redirect('login.html')
    context['username'] = request.session['username']

    headers = {'X-Auth-Token':request.session['tokenid']}
    #print(headers)
    images = requests.get(settings.GLANCE+'/v2/images',headers=headers)
    print(images)
    if images.status_code == 200:
        projects = requests.get(settings.KEYSTORN+'/v3/auth/projects',headers=headers)
        print(projects)
        if projects.status_code == 200:
            projectslist = projects.json()
            projectslist = projectslist['projects'] 
            plist={}
            for one in projectslist:
                plist[one['id']]=one['name']
            print('-----')
            print(plist)
            context['plist']=plist
        imageslist = images.json()
        if not imageslist.has_key('images'):
            return HttpResponse('查找错误，请稍后再试！')
        context['list'] = imageslist['images']
        # print(imageslist)
    else:
        return HttpResponse('查找错误，请稍后再试！')

    return render(request,'image.html',context)

def network(request):
    context={}
    if not (request.session.has_key('username') and request.session['username'] !=''):
       return redirect('login.html')
    context['username'] = request.session['username']

    headers = {'X-Auth-Token':request.session['tokenid']}
    networks = requests.get(settings.NEUTRON+'/v2.0/networks',headers = headers)
    if networks.status_code == 200:
        projects = requests.get(settings.KEYSTORN+'/v3/auth/projects',headers=headers)
        if projects.status_code == 200:
            projectslist = projects.json()
            projectslist = projectslist['projects'] 
            plist={}
            for one in projectslist:
                plist[one['id']]=one['name']
            context['plist']=plist    
        subnet = requests.get(settings.NEUTRON+'/v2.0/subnets',headers = headers)
        if subnet.status_code==200:
            subnet = subnet.json()
            # print(subnet)
            subnet1 = subnet['subnets']
            slist={}
            slist1 ={}
            for one in subnet1:
                slist[one['id']] =one['name'] 
                slist1[one['id']] = one['cidr']
            context['slist'] = slist 
            context['slist1'] = slist1     
        networklist = networks.json()
        if not networklist.has_key('networks'):
            return HttpResponse('查找错误，请稍后再试！')    
        context['list'] = networklist['networks']
        context['external'] = networklist['networks'][0]['router:external']
    else:
        return HttpResponse('查找错误，请稍后再试1！')

    return render(request,'network.html',context)

def instance(request):
    context={}
    if not (request.session.has_key('username') and request.session['username'] !=''):
       return redirect('login.html')
    context['username'] = request.session['username']
    headers = {'X-Auth-Token':request.session['tokenid']}
    instancesxx = requests.get(settings.NOVA+'/v2/servers/detail',headers = headers)
    if instancesxx.status_code == 200:
        print('-----')
        image = requests.get(settings.GLANCE+'/v2/images',headers = headers)
        if image.status_code == 200:
            image = image.json()
            image = image['images']
            ilist={}
            for one in image:
                ilist[one['id']]=one['name']
            context['ilist']=ilist
        instanceslist = instancesxx.json()
        #print(instanceslist)
        if not instanceslist.has_key('servers'):
            return HttpResponse('查找错误，请稍后重试！')
        ins =instanceslist['servers']    
        context['list'] = instanceslist['servers'] 
        for i in context['list']:
            image = i['image']
            key_name = i['key_name']
            availability_zone = i['OS-EXT-AZ:availability_zone']
            task_state = i['OS-EXT-STS:task_state']   
            power = i['OS-EXT-STS:power_state']  
            created =i['created']               
        context['image'] = image    
        context['created'] = created
        context['power'] = power
        flavor = requests.get(settings.NOVA+'/v2.1/flavors',headers=headers)
        if flavor.status_code==200:
            flavor = flavor.json()
            flavor = flavor['flavors']
            flist = {}
            for one in flavor:
                flist[one['id']] = one['name']
            context['flist'] = flist
        if key_name == None:
            context['key_name'] = "-"
        else:
            context['key_name'] = key_name    
        context['az'] = availability_zone 
        context['task'] = task_state                         
        print('----')

        image1 = requests.get(settings.GLANCE+'/v2/images',headers = headers)
        image1 = image1.json()
        # print(image1)
        context['image1'] = image1['images']
        flavors = requests.get(settings.NOVA+'/v2/flavors/detail',headers=headers)
        flavors = flavors.json()
        # print(flavors)
        context['flavors1'] = flavors['flavors']
        for f in context['flavors1']:
            ephemeral = f['OS-FLV-EXT-DATA:ephemeral']
            fpublic = f['os-flavor-access:is_public']
        context['ephemeral'] = ephemeral
        context['fpublic'] =fpublic
        networks = requests.get(settings.NEUTRON+'/v2.0/networks',headers = headers)
        subnet = requests.get(settings.NEUTRON+'/v2.0/subnets',headers = headers)
        if subnet.status_code==200:
            subnet = subnet.json()
            # print(subnet)
            subnet1 = subnet['subnets']
            slist={}
            slist1 ={}
            for one in subnet1:
                slist[one['id']] =one['name'] 
            context['slist'] = slist 
        networks = networks.json()
        context['networks'] = networks['networks']
        
    else:
        return HttpResponse('查找错误，请稍后重试！')

    return render(request,'instance1.html',context)
def create_ins(request):
    context = {}
    headers = {'X-Auth-Token':request.session['tokenid']}
    # if request.method == 'POST':
    # insname = request.POST.get('ins_name')
    # if insname == " ":
    #     return HttpResponse('请输入实例名！')
    # img_id = request.POST.get('img')
    # flavor_id = request.POST.get('flavor')
    # data = dumps.json(
    #     {
    #         "server" : {
    #             "accessIPv4": "1.2.3.4",
    #             "accessIPv6": "80fe::",
    #             "name" : insname,
    #             "imageRef" : img_id,
    #             "flavorRef" : flavor_id,
    #             "availability_zone": "us-west",
    #             "OS-DCF:diskConfig": "AUTO",
    #             "metadata" : {
    #                 "My Server Name" : "Apache1"
    #             },
    #             "personality": [
    #                 {
    #                     "path": "/etc/banner.txt",
    #                     "contents": "ICAgICAgDQoiQSBjbG91ZCBkb2VzIG5vdCBrbm93IHdoeSBp dCBtb3ZlcyBpbiBqdXN0IHN1Y2ggYSBkaXJlY3Rpb24gYW5k IGF0IHN1Y2ggYSBzcGVlZC4uLkl0IGZlZWxzIGFuIGltcHVs c2lvbi4uLnRoaXMgaXMgdGhlIHBsYWNlIHRvIGdvIG5vdy4g QnV0IHRoZSBza3kga25vd3MgdGhlIHJlYXNvbnMgYW5kIHRo ZSBwYXR0ZXJucyBiZWhpbmQgYWxsIGNsb3VkcywgYW5kIHlv dSB3aWxsIGtub3csIHRvbywgd2hlbiB5b3UgbGlmdCB5b3Vy c2VsZiBoaWdoIGVub3VnaCB0byBzZWUgYmV5b25kIGhvcml6 b25zLiINCg0KLVJpY2hhcmQgQmFjaA=="
    #                 }
    #             ],
    #             "security_groups": [
    #                 {
    #                     "name": "default"
    #                 }
    #             ],
    #             "user_data" : "IyEvYmluL2Jhc2gKL2Jpbi9zdQplY2hvICJJIGFtIGluIHlvdSEiCg=="
    #         },
    #         "OS-SCH-HNT:scheduler_hints": {
    #             "same_host": "48e6a9f6-30af-47e0-bc04-acaed113bb4e"
    #         }
    #     } )
    #     info = requests.post(settings.NOVA+'/v2/servers',data)
    #     if info.status_code == 200:
    #         return HttpResponse("启动实例成功")
    #     else:
    #         return HttpResponse("启动实例失败")

    return render(request,'instance1.html')

        


