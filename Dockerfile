FROM python:3.4.3
WORKDIR /code
COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt
RUN apt-get install nodejs
RUN apt-get install ruby
RUN npm install -g bower
RUN gem install bundler
ADD . /code
RUN cd /code/pygotham/frontend/static && bower install
RUN cd /code/pygotham/frontend/static && bundle install
