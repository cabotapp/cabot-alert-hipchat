Cabot Hipchat Plugin
=====

This is an alert plugin for the cabot service monitoring tool. It allows you to alert users by their user handle in a hipchat room.

## Installation

Install using pip

    pip install cabot-alert-hipchat

Edit `conf/production.env` in your Cabot clone to include the plugin:

    CABOT_PLUGINS_ENABLED=cabot_alert_hipchat...,<other plugins>

## Configuration

The plugin requires the following environment variables to be set:

    HIPCHAT_ALERT_ROOM=<room_id>
    HIPCHAT_API_KEY=your_hipchat_api_key
    
For self-hosted hipchat deployments you can also specify

    HIPCHAT_DOMAIN=api.my-hipch.at
    
Previous versions used `HIPCHAT_URL`. This is now deprecated.

If `HIPCHAT_URL` is set and `HIPCHAT_DOMAIN` isn't, the domain-name will be parsed from `HIPCHAT_URL`
