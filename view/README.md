# Posts analyser frontend
React frontend application.

## Run locally
### Prerequisites
- node ~v17.0.1 (npm ~v8.1.0)
- ClientID for registered Google auth application

### Settings
Set backend API address in `package.json`, for example:
```json
{
  "proxy": "http://localhost:8000"
}
```

### Development
```bash
export REACT_APP_GOOGLE_CLIENT_ID=<CLIENTID>
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### Production
1. Build app
```bash
npm run build
```

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

## Docker
### Development
**Build**  
Set port to backend in `package.json`. With no valid backend port provided the view will work, but no logic nor models will be available. Then run:

```bash
docker build --no-cache -t pa-front-dev:latest .
```

**Run**
```bash
docker run \
    -it \
    --rm \
    -p 3000:3000 \
    -e REACT_APP_GOOGLE_CLIENT_ID=<CLIENTID> \
    pa-front-dev:latest
```
Open http://localhost:3000 to view it in your browser.  


### Production
**Build**
Register Google Auth application at https://console.developers.google.com/apis/credentials
```bash
export REACT_APP_GOOGLE_CLIENT_ID=<CLIENT_ID>
```

```bash
docker build --build-arg REACT_APP_GOOGLE_CLIENT_ID=${REACT_APP_GOOGLE_CLIENT_ID} -f deploy/Dockerfile --no-cache -t pa-front:latest .
```

**Run**
Run docker compose from `<project_root>/deploy`.