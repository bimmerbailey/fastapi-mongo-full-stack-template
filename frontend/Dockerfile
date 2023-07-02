FROM node:18.2-alpine3.15 as build

WORKDIR /frontend

RUN npm install -g npm

COPY package*.json .

EXPOSE 3000

RUN yarn install

COPY . .

RUN yarn build

CMD ["sh", "-c", "npm rebuild esbuild && yarn dev"]

FROM nginx:1.23.3-alpine as production-build
COPY nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /frontend/dist /frontend

EXPOSE 80