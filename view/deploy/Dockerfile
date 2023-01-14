FROM node:13.12.0-alpine as build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm ci
RUN npm install react-scripts@3.4.1 -g

COPY . ./

RUN npm run build


FROM nginx:1.17.10
COPY --from=build /app/build /etc/nginx/html
COPY ./deploy/nginx.conf /etc/nginx/nginx.conf
COPY ./deploy/certs/localhost.crt /etc/ssl/localhost.crt
COPY ./deploy/certs/localhost.key /etc/ssl/localhost.key
CMD ["nginx", "-g", "daemon off;"]