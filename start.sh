#!/bin/sh

# Start cron service
service cron start

# Start the Flask app
python app.py
