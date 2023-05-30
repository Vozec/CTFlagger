FROM ubuntu:latest

#===== ENV ============================================
ENV DOMAIN ctflagger
ENV DOCUMENT_ROOT /var/www/${DOMAIN}

ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development


#===== FILES ==========================================

ADD ./app ${DOCUMENT_ROOT}
WORKDIR ${DOCUMENT_ROOT}

#===== DEPS OS=========================================

RUN \
    apt-get -y -qq update; \
    apt-get -y -qq upgrade; \
    apt-get -y -qq install --yes --fix-missing \
    python3 python3-pip python3-dev bash cron sudo nano unzip zip curl git wget file xxd libgl1; \
    sudo ln -s /usr/bin/python3 /usr/bin/python;

RUN \
    python -m pip install -r requirements.txt ;

#===== DEPS TOOLS======================================

RUN \
    chmod +x setup_tools.sh;\
    ./setup_tools.sh;
    
#===== SETUP ==========================================

# Crontab
RUN \    
    echo "@hourly server ${DOCUMENT_ROOT}/utils/auto-deletion.py" > /etc/cron.hourly/schedule ;\
    chmod +x ${DOCUMENT_ROOT}/utils/auto-deletion.py ;\
    chmod 600 /etc/cron.hourly/schedule ;

RUN \
    mkdir /tmp/${DOMAIN}; \
    echo "cd ${DOCUMENT_ROOT}" >> /root/.bashrc;

EXPOSE 5000
CMD ["flask","run"]

