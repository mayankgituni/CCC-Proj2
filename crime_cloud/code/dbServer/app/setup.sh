#!/usr/bin/env bash

export https_proxy="http://wwwproxy.unimelb.edu.au:8000"
export http_proxy="http://wwwproxy.unimelb.edu.au:8000"
export ftp_proxy="http://wwwproxy.unimelb.edu.au:8000"
export no_proxy="localhost,127.0.0.1,127.0.1.1,172.17.0.2,172.17.0.3,172.17.0.4,ubuntu"

python3 main.py
