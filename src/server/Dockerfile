FROM node:latest
ADD package.json package.json
RUN npm install
ADD . .
EXPOSE 3001
CMD ["npm", "start"]