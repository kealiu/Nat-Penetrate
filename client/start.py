import os
import uuid
import requests
from jinja2 import Environment, FileSystemLoader, Template

environment = Environment(loader=FileSystemLoader("."))
template = environment.get_template("frpc.tmpl")

FRPS_API=os.environ['FRPS_API']
FRPS_TOKEN=os.environ['FRPS_TOKEN']
FRPS_SEVER=os.environ['FRPS_SEVER']

def gen_frpc_conf(configs):
    with open('frpc.toml', 'w') as f:
        f.write(template.render(**configs))

def get_uuid():
    uuidfile = '.uuid'
    deviceuuid = uuid.uuid1().hex
    if os.path.isfile(uuidfile):
        with open(uuidfile) as f:
            deviceuuid = f.read()
    else:
        with open(uuidfile, 'w') as f:
            f.write(deviceuuid)
    return deviceuuid

def main():
    deviceuuid = get_uuid()
    response = requests.get(FRPS_API+'/api/reg/'+deviceuuid)
    frpcinfo = response.json()
    print(frpcinfo)
    frpcf = {
        'server': FRPS_SEVER,
        'servertoken': FRPS_TOKEN,
        'deviceuuid': deviceuuid,
        'remoteport': frpcinfo['nodeport'],
        'serverport': frpcinfo['serviceport']
    }
    gen_frpc_conf(frpcf)
    os.system('frpc -c frpc.toml')

if __name__ == '__main__':
    main()

