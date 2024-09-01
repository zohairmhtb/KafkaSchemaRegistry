FROM node:20.17.0

WORKDIR /app

COPY package*.json ./

RUN npm install -g @nestjs/cli
RUN npm install

COPY . .

RUN npm run build

CMD [ "npm", "run", "start:dev" ]