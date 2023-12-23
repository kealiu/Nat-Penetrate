# Client

This client will first generated `UUID` of device, and then register device with server, finally start NAT penetrate services client.

## Install

```bash
pip install -U Jinja2
```

## Start

### Environment Varibles

- `FRPS_API`: the services API
- `FRPS_TOKEN`: the token/password of services
- `FRPS_SEVER`: the server name of penetrace services

```bash
export FRPS_API='http://api.mydomain.com'
export FRPS_TOKEN='Secret'
export FRPS_SEVER='http://frp.mydomain.com'
python3 start.py
```
