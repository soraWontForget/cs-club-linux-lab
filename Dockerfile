FROM debian:bookworm-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        coreutils \
        hostname \
        less \
        man-db \
        manpages \
        ncurses-bin \
        python3 \
        tree \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash student

WORKDIR /opt/linux-basics-lab
COPY . /opt/linux-basics-lab
COPY docker/student.bashrc /home/student/.bashrc

RUN chmod +x /opt/linux-basics-lab/scripts/grade_part_*.py \
    && ln -s /opt/linux-basics-lab /home/student/lab \
    && chown -R student:student /opt/linux-basics-lab \
    && chown student:student /home/student /home/student/.bashrc \
    && chown -h student:student /home/student/lab

USER student

WORKDIR /home/student/lab

CMD ["/bin/bash"]
