# Server Demo API

## Install & Startup

### install

```bash
pip install -r requirements.txt
```

### environment varibles

- `FRP_SERVER_DOMAIN`: the basic domain name of devices. the final device domain will be `<device-uuid>.{FRP_SERVER_DOMAIN}`
- `FRP_SERVER_PORT`: the server application will listening in this port

### run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 9000
```

## APIs

- `/reg/{devuuid}` : register a new device with UUID
    - save device information in **Dynamodb**
    - generate Nginx configuration (or update AWS Application Load Balancer Rules)
- `/conn/{devuuid}` : connect to a exist device with UUID
    - fetch device information from **Dynamodb**
    - update Nginx configuration
    - generate connect URL and return HTTP redirect
- `/default/` : transfer UUID hostname to connect
    - transfer UUID host to `/conn/{devuuid}`
    - redirect to `/conn/{devuuid}`
