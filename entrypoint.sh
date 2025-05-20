#!/bin/bash

# Install requirements
pip install -r requirements.txt

# Jalankan server Pyramid
pserve production.ini --server-name main
