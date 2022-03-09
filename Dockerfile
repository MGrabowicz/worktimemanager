FROM python:3

ENV DockerHOME=/worktimemanager

RUN mkdir -p ${DockerHOME}

WORKDIR ${DockerHOME}

COPY . ${DockerHOME}

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
# install dependencies  
RUN pip install --upgrade pip  
# copy whole project to your docker home directory. COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  
RUN pip install Pillow
# port where the Django app runs  
EXPOSE 8000  
# start server  
# CMD python manage.py runserver  0.0.0.0:8000
