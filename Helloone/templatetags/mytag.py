#coding: utf-8
from django import template
from datetime import datetime
import time
register = template.Library()

@register.filter
def get_item(dictionary,key):
    return dictionary.get(key)

@register.filter
def time_since(value):
    # if not isinstance(value, datetime):
    #     return value
    value = datetime.strptime(value,'%Y-%m-%dT%H:%M:%SZ')   
    now = datetime.utcnow()
    timestamp = (now - value).total_seconds()
    if timestamp < 60:
        return '刚刚'
    elif timestamp >= 60 and timestamp < 60 * 60:
        minutes = int(timestamp/60)
        return '%s 分钟' % minutes
    elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
        if not int(timestamp%(60*60)) == 0:
            hours0 = int(timestamp/(60*60))
            min1 =int((timestamp-hours0*(60*60))/60)
            return "%s小时,"%hours0+"%s分钟"%min1
        else:    
            hours = int(timestamp/(60*60))
            return '%s 小时' % hours
    elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
        if not int(timestamp%(60*60*24)) == 0:
            day1 = int(timestamp/(60*60*24))
            hours1 =int((timestamp-day1*(60*60*24))/(60*60))
            return "%s天,"%day1+"%s小时"%hours1
        else:    
            days = int(timestamp /( 60* 60*24))
            return '%s 天' % days
    elif timestamp>60*60*24*30 and timestamp<60*60*24*30*12:
        if not int(timestamp%(60*60*24*30)) == 0:
            months1 = int(timestamp/(60*60*24*30))
            weeks1=int((timestamp-months1*(60*60*24*30))/(60*60*24*7))
            return "%s月,"%months1+"%s周"%weeks1
        else:    
            months = int(timestamp/(60*60*24*30))
            return "%s月"%months
    elif timestamp>60*60*24*30*12: 
        years = int(timestamp/(60*60*24*30*12))
        return "%s年"%years    
    else:
        return value.strftime('%Y/%m/%d %H:%M')

@register.filter
def power(value):
    if value ==0:
        return "NOSTATE"
    elif value == 1:
        return "RUNNING"
    elif value == 3:
        return "PAUSED"        
    elif value == 4:
        return "SHUTDOWN"
    elif value == 6:
        return "CRASHED"    
    else:
        return "SUSPENDED"

@register.filter
def time_tran(value):
    times = datetime.strptime(value,'%Y-%m-%dT%H:%M:%Sz')
    t = time.localtime(time.time())
    times = times.strftime('%Y-%m-%d %H:%M')
    return times 
@register.filter
def size_tran(value):
    #value = value
    if value<1000:
        return '%i'%value +'B'
    elif 1000<value<1000000:
        return '%.1f' %float(value/1000)+'KB'
    elif 1000000 <= value < 1000000000:
        return '%.2f' %float(value/(1024*1024)) + 'MB'
    elif 1000000000 <= value < 1000000000000:
        return '%.1f' %float(value/1000000000) + 'GB'
    elif 1000000000000 <= value:
        return '%.1f' %float(value/1000000000000) + 'TB'                

 
        