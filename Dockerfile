FROM python:3.7.2
COPY main_app /
COPY req.txt /
COPY gunicorn.conf /
RUN pip3 install --upgrade pip \
    && pip3 install -r req.txt \
    && pip3 install virtualenv
RUN python3 -m virtualenv --python=python3 virtualenv
CMD [ "gunicorn", "-c", "gunicorn.conf", "main:app" ]
