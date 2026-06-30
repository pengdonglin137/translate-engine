# 翻译项目构建环境
FROM ubuntu:20.04

# 安装基础工具
RUN apt-get update && apt-get install -y \
    texlive-xetex \
    texlive-lang-chinese \
    fonts-noto-cjk \
    python3 \
    python3-pip \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# 安装 pandoc
RUN wget -q https://github.com/jgm/pandoc/releases/download/2.9.2.1/pandoc-2.9.2.1-1-amd64.deb \
    && dpkg -i pandoc-2.9.2.1-1-amd64.deb \
    && rm pandoc-2.9.2.1-1-amd64.deb

# 安装 pandoc-crossref
RUN wget -q https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.16.0/pandoc-crossref-Linux.tar.xz \
    && tar xf pandoc-crossref-Linux.tar.xz \
    && mv pandoc-crossref /usr/local/bin/ \
    && rm pandoc-crossref-Linux.tar.xz

# 安装 Python 依赖
RUN pip3 install natsort pandoc-fignos pandoc-tablenos pyyaml

WORKDIR /workspace
