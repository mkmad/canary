FROM ubuntu:14.04
MAINTAINER Amit Gandhi <amit.gandhi@rackspace.com>

RUN apt-get -qq update
RUN apt-get -qq upgrade

# Install Pip, Python, etc
RUN apt-get -qqy install git-core wget curl libpython-dev libev4 libev-dev libffi6 libffi-dev libssl-dev python-dev

# setuptools
RUN wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
RUN python ez_setup.py

# pip
RUN wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
RUN python get-pip.py

# uwsgi 
RUN pip install uwsgi

# Pull project
RUN git clone https://github.com/rackerlabs/canary.git /home/canary

# Install Requirements
RUN sudo pip install -r /home/canary/requirements.txt

RUN sudo pip install -e /home/canary/.

# Set up the configuration files
ADD canary.conf /etc/canary.conf
ADD uwsgi.ini /root/uwsgi.ini

# Deploy the startup script
ADD startup.sh /usr/local/bin/canary_startup
RUN chmod 755 /usr/local/bin/canary_startup

# create uwsgi log directory
RUN mkdir -p /var/log/canary
RUN chmod -R +w /var/log/canary

# create uwsgi pid directory
RUN mkdir -p /var/run/canary
RUN chmod -R +w /var/run/canary

# Run the startup script     
RUN chmod 755 /usr/local/bin/canary_startup

EXPOSE 8080

# startup
CMD canary_startup
