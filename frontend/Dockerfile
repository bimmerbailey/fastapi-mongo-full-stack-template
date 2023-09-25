FROM node:18.2-alpine3.15 as base

WORKDIR /frontend

COPY package*.json .
RUN yarn install

COPY . .

FROM base as development
EXPOSE 3000

ENTRYPOINT yarn dev

FROM base as build
RUN yarn build

FROM nginx:1.23.3-alpine as production
COPY nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /frontend/dist /frontend

EXPOSE 80