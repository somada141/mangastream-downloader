FROM continuumio/miniconda:latest
RUN conda install -y pip lxml
ADD . /mangastream-downloader
RUN mkdir "/tmp/mangastream_downloader"
RUN chmod 777 "/tmp/mangastream_downloader"
WORKDIR /mangastream-downloader
RUN pip install -r requirements.txt
CMD python mangastream.py rss --no-overwrite