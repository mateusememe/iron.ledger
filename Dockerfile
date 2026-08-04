# Stage 1: Build the Stlite static bundle
FROM python:3.10-slim AS builder

WORKDIR /app

# Copy the necessary source files
COPY iron_ledger/ iron_ledger/
COPY web/ web/
COPY build_static.py .

# Run the build script to generate dist/index.html
RUN python build_static.py

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy the static output from the builder
COPY --from=builder /app/dist/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
