# osta-exporter

A custom [Prometheus exporter][] for exporting metrics from [osta.ee][] ebay-like auction platform.

## Usage

This is designed to be run in a Docker container. Deploy it to your Docker platform of choice.
The exporter will listen on port `8080`.

```bash
$ docker run -p 8080:8080 anroots/osta-exporter
```

Configure a new Prometheus target to scrape the exposed endpoint.

```yaml
scrape_configs:
  - job_name: 'osta-ee'
    scrape_interval: 30m
    static_configs:
      - targets:
        - osta-exporter:8080
 
```

The following metrics will be saved:

```

```

### Environment variables

| Variable name | Description | Default value | Required | 
| ------------- | ----------- | ------------- | -------- |
| OSTA_USER_ID| User ID in the osta.ee system whose metrics to export. Numeric. Get it from URL of your public profile| `None` | Yes |
| LOG_LEVEL| Exporter log level (to stdout)| `INFO` | No |


## Development

Use the included `docker-compose.yml` file for development..

```bash
$ docker-compose up
```

...or install dependencies to Python venv, and debug locally:

```bash
$ pip install -r requirements.txt
$ python src/collector.py
```

## References

- https://api.osta.ee/api

[Prometheus exporter]: https://prometheus.io/docs/instrumenting/writing_exporters/
[osta.ee]: https://osta.ee
