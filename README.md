# Marketplace Backend Assignment

## Development env setup

```bash
py -m venv environment
source ./environment/Scripts/activate // linux
./environment/Scripts/Activate.ps1 // windows
```

## Install dependencies

```bash
pip install -r ./requirements.txt
```

## Run server

```bash
uvicorn app.init:app --reload
```

## Endpoints

### GET **/auction/list**

Get all auction list

### GET **/auction/{id}**

Get auction data

### PUT **/auction/{id}**

Put bid to auction

### POST **/auction**

Create new auction