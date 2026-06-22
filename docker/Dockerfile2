FROM ubuntu:18.04

# Install essential packages
RUN apt-get update \
    && apt-get install -y nginx vim curl wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Configure nginx
RUN echo "server { \
        listen 80; \
        server_name localhost; \
        location / { \
            root /usr/share/nginx/html; \
            index index.html; \
        } \
    }" > /etc/nginx/nginx.conf

# Create a directory and download a sample webpage
RUN mkdir /usr/share/nginx/html/mywebsite \
    && wget -O /usr/share/nginx/html/mywebsite/index.html https://example.com/index.html

# Add some content to the webpage
RUN echo "<html><body><h1>Welcome to My Website!</h1></body></html>" >> /usr/share/nginx/html/mywebsite/index.html

WORKDIR /app

# Run nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]

