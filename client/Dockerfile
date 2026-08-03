FROM node:26

WORKDIR /app

COPY ./package-lock.json ./package.json ./

RUN npm ci

COPY ./ ./

CMD ["npm", "run", "dev"]
