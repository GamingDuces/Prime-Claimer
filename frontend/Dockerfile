FROM node:20-alpine

WORKDIR /app

COPY package.json vite.config.js ./
COPY ./public ./public
COPY ./src ./src

RUN npm install && npm run build
RUN npm install -g serve

ENV PORT=5173
EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "0.0.0.0:${PORT}"]
# This Dockerfile sets up a Node.js environment for a frontend application using Vite.
# It installs dependencies, builds the application, and serves it using the `serve` package.