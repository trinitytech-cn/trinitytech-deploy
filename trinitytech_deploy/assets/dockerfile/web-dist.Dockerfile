FROM joseluisq/static-web-server:2-alpine

ARG DIST=dist

COPY $DIST /public

EXPOSE 80
