FROM node:9.5.0
ADD package.json package.json
RUN npm install
ADD . .
EXPOSE 3001
CMD ["npm", "run", "start:prod"]