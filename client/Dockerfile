FROM node:26 AS builder

WORKDIR /app/client

COPY ./client/package.json ./client/package-lock.json ./client/.npmrc ./

RUN npm ci

COPY ./client/ ./

RUN npm run build-only


FROM caddy:2.11

COPY ./client/Caddyfile /etc/caddy/Caddyfile

COPY --from=builder /app/client/dist /usr/client/
