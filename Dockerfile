################################
# Docker file for Sclust analysis
# Base on Ubuntu 16.04
################################

FROM ubuntu:16.04

#Developer/maintainer
MAINTAINER Apiwat Sangphukieo

RUN apt-get update && apt-get install -y \
	make \
	gcc \
	g++ \
	zlib1g \
	zlib1g-dev \
	python3 \
	r-base-core \
	wget
	
# Download Sclust
RUN wget --no-verbose http://www.uni-koeln.de/med-fak/sclust/Sclust.tgz -O "Sclust.tgz" && \
    tar zxvf Sclust.tgz

RUN cd Sclust/src && \
	make -f makefile.ubuntu TARGET=NEHALEM && \
	cd /

RUN wget --no-verbose https://raw.githubusercontent.com/asangphukieo/sclust/main/script/preprocess_vcf_sclust.py -O "preprocess_vcf_sclust.py"

ENV sclust="Sclust/bin/Sclust"

RUN rm Sclust.tgz
