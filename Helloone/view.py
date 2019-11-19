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
        #print(info['token']*)
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
    images = requests.get(settings.IMAGES+'/v2/images',headers=headers)
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
        print(imageslist)
    else:
        return HttpResponse('查找错误，请稍后再试1！')

    return render(request,'image.html',context)

def network(request):
    context={}
    if not (request.session.has_key('username') and request.session['username'] !=''):
       return redirect('login.html')
    context['username'] = request.session['username']

    headers = {'X-Auth-Token':request.session['tokenid']}
    networks = requests.get(settings.NETWORK+'/v2.0/networks',headers = headers)
    #print(networks)
    if networks.status_code == 200:
        projects = requests.get(settings.KEYSTORN+'/v3/auth/projects',headers=headers)
        if projects.status_code == 200:
            projectslist = projects.json()
            projectslist = projectslist['projects'] 
            plist={}
            for one in projectslist:
                plist[one['id']]=one['name']
            print('-----')
            #print(plist)
            context['plist']=plist    
        networklist = networks.json()
        print(networklist)
        if not networklist.has_key('networks'):
            return HttpResponse('查找错误，请稍后再试！')
        context['list'] = networklist['networks']
    else:
        return HttpResponse('查找错误，请稍后再试1！')

    return render(request,'network.html',context)

#def addnetwork(request):
#    context={}
#    if not (request.session.has_key('username') and request.session['username'] !=''):
#       return redirect('login.html')
#    context['username'] = request.session['username']
#    return render(request,'addnetwork.html',context)    

def instance(request):
    context={}
    if not (request.session.has_key('username') and request.session['username'] !=''):
       return redirect('login.html')
    context['username'] = request.session['username']
    headers = {'X-Auth-Token':request.session['tokenid']}
    # instance = requests.get(settings.INSTANCE+'/v2.1/servers',headers = headers)
    # instance = instance.json()
    # ins_id = instance['servers'] [0]['id']
    # #print(instance)
    # #print(ins_id)
    # print('-----')
    # ins = requests.get(settings.INSTANCE+'/v2.1/servers',headers = ins_id)
    # ins = ins.json()
    # print(ins)
    instancesxx = requests.get(settings.INSTANCE+'/v2/servers/detail',headers = headers)
    if instancesxx.status_code == 200:
        print('-----')
        image = requests.get(settings.IMAGES+'/v2/images',headers = headers)
        if image.status_code == 200:
            image = image.json()
            image = image['images']
            ilist={}
            for one in image:
                ilist[one['id']]=one['name']
            context['ilist']=ilist
        instanceslist = instancesxx.json()
        print(instanceslist)
        if not instanceslist.has_key('servers'):
            return HttpResponse('查找错误，请稍后重试！')
        context['list'] = instanceslist['servers'] 
        context['image'] =  instanceslist['servers'][0]['image']
        ins_id = instanceslist['servers'][0]['id']
        print(ins_id)
        context['address'] = instanceslist['servers'][0]['addresses']['provider'][0]['addr']
        context['name1'] = instanceslist['servers'][0]['name']
        flavor = requests.get(settings.INSTANCE+'/v2.1/flavors',headers=headers)
        if flavor.status_code==200:
            flavor = flavor.json()
            print(flavor)
            flavor = flavor['flavors']
            flist = {}
            for one in flavor:
                flist[one['id']] = one['name']
            context['flist'] = flist
            request.session['flist'] = flist
            request.session['flavor'] = flavor
        flavor1 = instanceslist['servers'][0]['flavor']
        context['flavor'] = flavor1 
        #request.session['id'] = flavor1 
        key_name = instanceslist['servers'][0]['key_name']
        if key_name == None:
            context['key_name'] = "-"
        else:
            context['key_name'] = key_name    
        context['az'] = instanceslist['servers'][0]['OS-EXT-AZ:availability_zone'] 
        context['task'] = instanceslist['servers'][0]['OS-EXT-STS:task_state']
        power = instanceslist['servers'][0]['OS-EXT-STS:power_state']  
        if power ==0:
            context['power'] ="NOSTATE"
        elif power == 1:
            context['power'] = "RUNNING"
        elif power == 3:
            context['power'] = "PAUSED"        
        elif power == 4:
            context['power'] ="SHUTDOWN"
        elif power == 6:
            context['power'] = "CRASHED"    
        else:
            context['power'] ="SUSPENDED"                          
        print('----')
        created = instanceslist['servers'][0]['created']
        #context['created'] = dateutil.parser.parse(created)
        context['created'] = datetime.strptime(created,'%Y-%m-%dT%H:%M:%SZ')
        print('----')
        #print(context['created']) 
    else:
         return HttpResponse('查找错误，请稍后重试！')
    return render(request,'instance1.html',context) 

def addinstance(request):
    context = {}
    
    return render(request,'addinstance.html',context)



