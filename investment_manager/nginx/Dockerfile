FROM nginx:latest

COPY ./default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Start Nginx in the foreground when the container runs
CMD ["nginx", "-g", "daemon off;"]
