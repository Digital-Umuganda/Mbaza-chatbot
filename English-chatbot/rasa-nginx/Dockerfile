FROM nginx:alpine
RUN apk update && apk add bash
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Africa/Kigali /etc/localtime
COPY ./ /usr/share/nginx/html
COPY ./disti/ /usr/share/nginx/html/dist
COPY ./static /usr/share/nginx/html/static
