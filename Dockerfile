FROM ubuntu:latest

#===== ENV ============================================
ENV ZIPFILE source.zip
ENV DOMAIN ctfilescan
ENV DOCUMENT_ROOT /var/www/${DOMAIN}
ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

#======================================================

#===== FILES / USER / DEPS ============================
COPY ${ZIPFILE} /tmp/${ZIPFILE}

RUN \
	# APT ;\
	apt-get -y -qq update; \
	apt-get -y -qq upgrade; \

	# INIT INSTALL ;\
	apt-get -y -qq install  --yes \
	python3 python3-pip	python3-dev bash sudo nano unzip zip curl git wget file xxd tshark default-jdk \
	binutils binwalk openssl 2to3 sox cargo rubygems pdfcrack stegsnow outguess strace ltrace checksec \
	ssldump exiftool pngcheck john ffmpeg;\

	# WEBSERVER FILES ;\ 
	rm -rf /var/www/html/; \
	mkdir -p ${DOCUMENT_ROOT}; \
	mv /tmp/${ZIPFILE} ${DOCUMENT_ROOT}/${ZIPFILE}; \
	unzip ${DOCUMENT_ROOT}/${ZIPFILE} -d /var/www/${DOMAIN}; \
    echo "cd ${DOCUMENT_ROOT}" >> /root/.bashrc; \

    # USERS ;\ 
    rm ${DOCUMENT_ROOT}/${ZIPFILE}; \
    useradd -m -s /bin/bash server; \
    echo "server:server" | chpasswd; \
    echo "root:Th1sIsTh3R0oTP@sswd123" | chpasswd; \
	
	# PYTHON DEPS ;\
	sudo ln -s /usr/bin/python3 /usr/bin/python ;\
	python3 -m pip install -r /var/www/${DOMAIN}/requirements.txt ;\

	# MODULES DEPS ;\
	mkdir /opt/tools/ && cd /opt/tools/ ;\

	# rockyou.txt ;\
	wget https://github.com/praetorian-inc/Hob0Rules/raw/master/wordlists/rockyou.txt.gz -O /tmp/rockyou.txt.gz ;\
	gzip -d /tmp/rockyou.txt.gz ;\
	mkdir -p /usr/share/wordlists/ ;\
	mv /tmp/rockyou.txt /usr/share/wordlists/rockyou.txt ;\

	# dtmf ;\
	git clone https://github.com/ribt/dtmf-decoder.git dtmf ;\
	cd dtmf/ ;\
	chmod +x dtmf.py ;\
	sudo cp dtmf.py /usr/local/bin/dtmf ;\

	# hideme ;\
	mv /var/www/${DOMAIN}/modules/resources/hideme /usr/bin/hideme ;\
	chmod +x /usr/bin/hideme ;\

	# pdf-parser ;\
	wget https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/pdf-parser.py -O /usr/bin/pdf-parser ;\
	chmod +x /usr/bin/pdf-parser ;\

	# steg86 ;\
	cargo install steg86 ;\
	cp /root/.cargo/bin/steg86 /usr/bin/ ;\

	# chainbreaker ;\
	git clone https://github.com/n0fate/chainbreaker.git /opt/tools/chainbreaker ;\
	echo -e '#!/bin/bash\npython3 /opt/tools/chainbreaker/chainbreaker.py ${@}' > /usr/bin/chainbreaker ;\
	chmod +x /usr/bin/chainbreaker ;\
	2to3 /opt/tools/chainbreaker/chainbreaker.py -W ;\
	
	# zsteg ;\
	gem install zsteg ;\
	gem install zsteg ;\

	# jsteg ;\
	wget https://github.com/lukechampine/jsteg/releases/download/v0.3.0/jsteg-linux-amd64 -O /usr/bin/jsteg ;\
	chmod +x /usr/bin/jsteg	;\

	# stegdetect ;\
	wget http://old-releases.ubuntu.com/ubuntu/pool/universe/s/stegdetect/stegdetect_0.6-6_amd64.deb -O /tmp/stegdetect.deb ;\
	apt-get -y -qq install /tmp/stegdetect.deb ;\
	rm /tmp/stegdetect.deb ;\

	# stegexpose ;\
	wget https://github.com/b3dk7/StegExpose/raw/master/StegExpose.jar -O /opt/tools/StegExpose.jar ;\
	echo -e '#!/bin/bash\njava -jar /opt/tools/StegExpose.jar ${@}' > /usr/bin/StegExpose ;\
	chmod +x /usr/bin/StegExpose ;\

	# stegoveritas ;\
	stegoveritas_install_deps ;\
	
	# stegseek ;\
	wget https://github.com/RickdeJager/stegseek/releases/download/v0.6/stegseek_0.6-1.deb -O /tmp/stegseek.deb ;\
	apt-get -y -qq install /tmp/stegseek.deb ;\
	rm /tmp/stegseek.deb ;\

	# stegolsb ;\
	wget https://gist.githubusercontent.com/dhondta/d2151c82dcd9a610a7380df1c6a0272c/raw/stegolsb.py -O /usr/bin/stegolsb ;\
	chmod +x /usr/bin/stegolsb ;\

	# stegopvd ;\
	wget https://gist.githubusercontent.com/dhondta/feaf4f5fb3ed8d1eb7515abe8cde4880/raw/stegopvd.py -O /usr/bin/stegopvd ;\
	chmod +x /usr/bin/stegopvd ;\
	
	# stegopit ;\
	wget https://gist.githubusercontent.com/dhondta/30abb35bb8ee86109d17437b11a1477a/raw/stegopit.py -O /usr/bin/stegopit ;\
	chmod +x /usr/bin/stegopit ;\

	# openstego ;\
	wget https://github.com/syvaidya/openstego/releases/download/openstego-0.8.5/openstego_0.8.5-1_all.deb -O /tmp/openstego.deb ;\
	apt install /tmp/openstego.deb ;\
	rm /tmp/openstego.deb ;

	# CLEAN ;\
	# apt-get autoremove -y ;\
	# apt-get clean ;\
	# rm -rf /var/lib/apt/lists/* ;
#======================================================


#===== SETUP ==========================================
VOLUME ${DOCUMENT_ROOT}
WORKDIR ${DOCUMENT_ROOT}

EXPOSE 8080
EXPOSE 80

CMD ["python3","app.py"]
#======================================================
