import os
import socket
import random
import boto3
import uuid

from boto3.dynamodb.conditions import Key

from typing import Union, Annotated
from fastapi import FastAPI, Request, Header
from fastapi.responses import RedirectResponse

from jinja2 import Environment, FileSystemLoader, Template

environment = Environment(loader=FileSystemLoader("."))
template = environment.get_template("nginx.conf.tmpl")

FRP_SERVER_DOMAIN=os.environ['FRP_SERVER_DOMAIN']
FRP_SERVER_PORT = int(os.environ['FRP_SERVER_PORT'])

app = FastAPI()

ddb = boto3.resource('dynamodb').Table('frp-server-db')

PORT_MAX=60000
PORT_MIN=30000

def ddb_putitem(item):
    ddb.put_item(Item=item)

def ddb_getitem(deviceuuid):
    dev = ddb.query(Select='ALL_ATTRIBUTES', KeyConditionExpression=Key('deviceuuid').eq(deviceuuid))
    if dev['Count'] < 1:
        return None
    return dev['Items'][0]

def nginx_update_conf(dev):
    ngconf=dev['deviceuuid']+".conf"
    with open(ngconf, 'w') as f:
        f.write(template.render(**dev, serverdomain=FRP_SERVER_DOMAIN))
    os.system("sudo rm -rf /etc/nginx/sites-enabled/%s && sudo mv -f %s /etc/nginx/sites-enabled/ && sudo systemctl reload nginx"%(ngconf, ngconf))

def get_local_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr

@app.get("/reg/{devuuid}")
def device_reg(devuuid: str, request: Request):
    nodeport = random.randrange(PORT_MIN, PORT_MAX)
    dev = {'deviceuuid': devuuid,
            'deviceip': request.client.host,
            'nodeip': get_local_ip(),
            'nodeport': nodeport,
            'serviceport': FRP_SERVER_PORT}
    nginx_update_conf(dev)
    ddb_putitem(dev)
    return dev

@app.get("/conn/{devuuid}")
def device_conn(devuuid: str, request: Request):
    # fetch uuid, write nginx conf, restart nginx
    dev = ddb_getitem(devuuid)
    if not dev:
        raise HTTPException(status_code=404, detail="Device UUID not found")
    print(dev)
    nginx_update_conf(dev)
    return RedirectResponse("http://"+devuuid+"."+FRP_SERVER_DOMAIN)

@app.get("/default/")
def device_conn(host: Annotated[str | None, Header()] = None):
    deviceuuid = host.split('.')[0]
    print(host, deviceuuid)
    try:
        print(host, deviceuuid)
        uuid.UUID(deviceuuid)
        return RedirectResponse('/conn/'+deviceuuid)
    except ValueError:
        return RedirectResponse('/index.html')

