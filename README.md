# hydro-tools-gui

GUI and REST APIS that sit on top of various hydraulic engineering tools. REST API provides parameter validation. GUI provides graphing functionality. Provides API for following tools:

 - [OCUSF](https://github.com/KevinGoode/ocusf)

![Image of hydro-tools-gui](https://github.com/KevinGoode/hydro-tools-gui/blob/master/screenshot.png)

## Build
```console
docker build -t hydro-tools-gui:latest .
```

## Run
```console
docker container run -it -p 80:80 -d hydro-tools-gui:latest
```

