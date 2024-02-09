FROM node:18.2
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
RUN npm install -g live-server
CMD [ "node", "server.js" ]
