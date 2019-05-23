FROM nginx:1.13.8-alpine

MAINTAINER ops@rockalabs.com

# Create logs files
RUN mkdir -p /etc/nginx/logs && \
	touch /etc/nginx/logs/site.access && \
	touch /etc/nginx/logs/site.error

# Copy custom configuration files
COPY compose/stage/nginx/nginx.conf /etc/nginx/nginx.conf
COPY compose/stage/nginx/default.conf /etc/nginx/conf.d/default.conf

# Run nginx
CMD nginx -g 'daemon off;'
