FROM node:26

WORKDIR /app

COPY ./package-lock.json ./package.json ./.npmrc ./

RUN npm ci

COPY ./ ./

CMD ["npm", "run", "dev"]
