
# +-------------------------------------------------------------------------------+
# | sudo docker build -t myblacksloth/pyytdownloader --progress=plain .           |
# |                                                                               |
# | sudo docker run --name pytdw -d -it -p 8070:8070 myblacksloth/pyytdownloader  |
# |                                                                               |
# +-------------------------------------------------------------------------------+
# sudo docker build --progress=plain --no-cache .
# sudo docker build --progress=plain .

# +----------------------------------------+
# |  sudo docker exec -it pytdw /bin/bash  |
# |                                        |
# +----------------------------------------+


# +-------------------------------------------------------+
# |                                                       |
# |   sudo docker stop pytdw                              |
# |   sudo docker rm pytdw                                |
# |   sudo docker image rm myblacksloth/pyytdownloader    |
# |   sudo docker buildx prune -f                         |
# |   sudo docker image prune -a                          |
# |                                                       |
# |                                                       |
# +-------------------------------------------------------+

FROM ubuntu:latest

EXPOSE 8070

SHELL ["/bin/bash", "-ec"]

RUN apt-get update && apt-get install -y wget ffmpeg python3 python3-pip python3-venv
RUN wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
RUN chmod +x /usr/local/bin/yt-dlp

# copy non copia le directory ma solo eventuali file nelle directory
# COPY . /downloader
RUN mkdir -p /downloader
COPY requirements.txt /downloader
# ---------
# COPY src/ /downloader
RUN mkdir -p /downloader/src
COPY src/ /downloader/src

WORKDIR /downloader

RUN ls -Rlsah

RUN python3 -m venv venv

# RUN source venv/bin/activate
# RUN ["/bin/bash", "-c", "source", "venv/bin/activate"]
RUN pip3 install -r requirements.txt

# RUN python3 -m src.main

CMD ["python3", "-m", "src.main"]

