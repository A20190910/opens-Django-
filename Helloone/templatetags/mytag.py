#coding: utf-8
from django import template
from datetime import datetime
register = template.Library()

@register.filter
def get_item(dictionary,key):
    return dictionary.get(key)

@register.filter
def time_since(value):
    if not isinstance(value, datetime):
        return value
    now = datetime.now()
    timestamp = (now - value).total_seconds()
    if timestamp < 60:
        return '刚刚'
    elif timestamp >= 60 and timestamp < 60 * 60:
        minutes = int(timestamp / 60)
        return '%s 分钟' % minutes
    elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
        hours = int(timestamp / 60 / 60)
        return '%s 小时' % hours
    elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
        days = int(timestamp / 60 / 60 / 24)
        return '%s 天' % days
    elif timestamp>60*60*24*30 and timestamp<60*60*24*30*12:
        if not int(timestamp%(60*60*24*30)) == 0:
            months = int(timestamp/(60*60*24*30))
            weeks=int((timestamp-months*(60*60*24*30))/(60*60*24*7))
            return "%s月,"%months+"%s周"%weeks
        else:    
            months = int(timestamp/(60*60*24*30))
            return "%s月"%months
    elif timestamp>60*60*24*30*12: 
        years = int(timestamp/(60*60*24*30*12))
        return "%s年"%years    
    else:
        return value.strftime('%Y/%m/%d %H:%M')

@register.filter
def trans(value):
    words = value.encode('utf-8').isalpha()
 
        