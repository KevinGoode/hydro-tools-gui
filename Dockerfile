# Alpine Base image for hydro-tools-gui
# docker build -t hydro-tools-gui:latest .
# docker container run  -it -p 80:80 -d hydro-tools-gui:latest
# FOR GUI DEV RUN AS:
# docker container run  -it -v /home/goode/Dev/hydro-tools-gui/gui:/var/www -p 80:80 -d hydro-tools-gui:latest
# docker container exec -it <container-id> /bin/sh
#FROM alpine
FROM nginx:alpine
RUN apk add --no-cache libc6-compat
RUN apk add --no-cache g++
RUN apk add --no-cache git
RUN apk add --no-cache python3
RUN apk add --no-cache py3-pip
RUN pip3 install flask
RUN pip3 install jsonschema
RUN apk add --no-cache nano
RUN mkdir /usr/lib/python3.8/site-packages/hydro_tools
# Install python app, gui and nginx config
COPY hydro_tools /usr/lib/python3.8/site-packages/hydro_tools
# COMMENT OUT FOLLOWING LINE WHEN DOING GUI DEV
COPY gui /var/www
COPY etc/nginx/conf.d /etc/nginx/conf.d
COPY etc/nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY bin/hydro-tools-gui.sh /bin/hydro-tools-gui.sh
RUN chmod a+rwx /bin/hydro-tools-gui.sh
# Get ocusf and build to /ocusf.exe
RUN git clone https://github.com/KevinGoode/ocusf.git
RUN g++ ocusf/OCUSF.cpp -o /ocusf/ocusf.exe
RUN mkdir -p /ocusf/sims
RUN chmod a+rwx /ocusf/sims
# Can only run one service by default in docker so need to wrap REST API and nginx execution inside script
CMD ["/bin/hydro-tools-gui.sh"]
