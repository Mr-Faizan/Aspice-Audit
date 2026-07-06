# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20-slim AS build-stage

WORKDIR /app

# Install dependencies needed for some node packages
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY package.json bun.lock /app/
COPY frontend/package.json /app/frontend/

WORKDIR /app/frontend

# Use npm to install for a robust build environment
RUN npm install

COPY ./frontend /app/frontend
ARG VITE_API_URL

# Build the production app
RUN npm run build


# Stage 1, based on Nginx, to have only the compiled app
FROM nginx:1

COPY --from=build-stage /app/frontend/dist/ /usr/share/nginx/html

COPY ./frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./frontend/nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
