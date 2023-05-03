FROM ubuntu:latest

RUN set -x \
    && ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone

# Latex packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        xzdec \
        git-core \
        python3-pip \
        texlive-latex-recommended \
        texlive-fonts-recommended \
        texlive-latex-extra \
        texlive-fonts-extra \
        texlive-lang-french && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Default command
CMD [ "python3", "/root/script/loop.py" ]
