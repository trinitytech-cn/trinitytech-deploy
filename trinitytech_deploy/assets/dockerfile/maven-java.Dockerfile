FROM ghcr.io/trinitytech-cn/openjdk-with-dejavu:8-jre-alpine3.9

ARG JAR_FILE

COPY $JAR_FILE /app/app.jar

EXPOSE 8080

CMD java -jar /app/app.jar
