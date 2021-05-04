# api

## requirements

### fastapi

### uvicorn
```
uvicorn main:app
--port INTEGER                  Bind socket to this port.  [default: 8000]
--reload                        Enable auto-reload.
```

### deploy
```
cd apipy
nohup uvicorn main:app --port 5910 &
pkill uvicorn
```
