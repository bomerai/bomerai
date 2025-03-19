# Use official Go runtime as base image
FROM golang:1.24.1-bullseye

# Set working directory
WORKDIR /app

# Install dependencies for libdxfrw (dwg2dxf)
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    autoconf \
    automake \
    libtool \
    cmake \
    libboost-dev \
    && rm -rf /var/lib/apt/lists/*

# Install libdxfrw (includes dwg2dxf)
RUN git clone https://github.com/LibreCAD/libdxfrw.git /tmp/libdxfrw \
    && cd /tmp/libdxfrw \
    && autoreconf -i \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && ldconfig \
    && rm -rf /tmp/libdxfrw

# Verify dwg2dxf installation
RUN /usr/local/bin/dwg2dxf --version || (echo "dwg2dxf not found or not working"; exit 1)

# Install Air for hot reloading
RUN go install github.com/air-verse/air@latest

# Copy go.mod and go.sum first to leverage Docker cache
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Use air for hot reloading in development
CMD ["air", "-c", ".air.toml"]