
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/configfile.template

COPY ./dist /usr/share/nginx/html

ENV PORT 8069
ENV HOST 0.0.0.0
EXPOSE 8069
CMD sh -c "envsubst '\$PORT' < /etc/nginx/conf.d/configfile.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
