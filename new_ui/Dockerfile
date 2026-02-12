FROM node:20-alpine3.20 AS base

WORKDIR /frontend

COPY package*.json .
RUN npm install

COPY . .

FROM base AS development
EXPOSE 3000

ENTRYPOINT npm run dev

FROM base AS build
RUN npm run build

FROM nginx:1.27-alpine AS production
COPY nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /frontend/dist /frontend

EXPOSE 80