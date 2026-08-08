FROM node:26 AS builder

WORKDIR /app/client

COPY ./package.json ./package-lock.json ./.npmrc ./

RUN npm ci

COPY ./ ./

RUN npm run build-only


FROM caddy:2.11

COPY ./Caddyfile /etc/caddy/Caddyfile

COPY --from=builder /app/client/dist /usr/client/
