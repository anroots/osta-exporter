FROM python:3.8-slim
LABEL io.openshift.tags=prometheus,prometheus-exporter,osta.ee \
    io.k8s.description="A prometheus exporter for metrics of osta.ee auction system" \
    maintainer="Ando Roots <ando@sqroot.eu>"

EXPOSE 8080
WORKDIR /opt/osta-exporter
ENV PYTHONPATH '/opt/osta-exporter/'

COPY requirements.txt /opt/osta-exporter/requirements.txt
RUN pip install -r /opt/osta-exporter/requirements.txt && \
    rm -f /opt/osta-exporter/requirements.txt
COPY src /opt/osta-exporter/src

CMD ["python" , "/opt/osta-exporter/src/collector.py"]
