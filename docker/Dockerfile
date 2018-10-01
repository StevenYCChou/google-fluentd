FROM debian:9.5-slim

COPY entrypoint.sh Dockerfile VERSION *.gem /
# TODO: This may be a moving target, figure out how to pin.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gnupg2 \
        lsb-release \
        build-essential \
        procps \
        systemd \
        ca-certificates \
        adduser \
    # Install google-fluentd at version 1.5.36-1.
    && curl -sS https://dl.google.com/cloudagents/install-logging-agent.sh | REPO_SUFFIX=20180915-1 DO_NOT_INSTALL_CATCH_ALL_CONFIG=true bash \
    # If any additional gems need to be installed, it should happen before the
    # image cleanup.
    # ==> INSTALL_ADDITIONAL_GEMS_HERE_IF_NEEDED <==
    && /opt/google-fluentd/embedded/bin/gem uninstall -ax --force \
        aws-sdk \
        aws-sdk-core \
        aws-sdk-resources \
        mime-types-data \
        mime-types \
        public_suffix \
        cool.io \
        google-api-client \
        google-cloud-core \
        google-cloud-env \
        google-cloud-logging \
        google-protobuf \
        googleauth \
        parallel \
        rubyzip \
        signet \
        stackdriver-core \
        fluentd \
        fluent-plugin-google-cloud \
        json \
    && /opt/google-fluentd/embedded/bin/gem install --no-ri --no-rdoc \
        json:1.8.6 \
        aws-sdk-resources:2.11.105 \
        aws-sdk-core:2.11.105 \
        aws-sdk:2.11.105 \
        mime-types-data:3.2016.0521 \
        mime-types:3.1 \
        public_suffix:3.0.2 \
        signet:0.8.1 \
        cool.io:1.4.4 \
        googleauth:0.6.4 \
        google-api-client:0.23.4 \
        google-cloud-env:1.0.2 \
        google-cloud-core:1.2.2 \
        stackdriver-core:1.3.0 \
        google-protobuf:3.5.1 \
        google-cloud-logging:1.5.1 \
        parallel:1.12.1 \
        rubyzip:1.2.1 \
        fluentd \
        fluent-plugin-google-cloud:0.7.0.pre.4 \
    && sed -i "s/num_threads 8/num_threads 8\n  detect_json true\n  # Enable metadata agent lookups.\n  enable_metadata_agent true\n  metadata_agent_url \"http:\/\/local-metadata-agent.stackdriver.com:8000\"/" "/etc/google-fluentd/google-fluentd.conf"

ENV LD_PRELOAD=/opt/google-fluentd/embedded/lib/libjemalloc.so


ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/sbin/google-fluentd"]
