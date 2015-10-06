Cabot Hipchat Plugin
=====

This is an alert plugin for the cabot service monitoring tool. It allows you to alert users by their user handle in a hipchat room.

## Installation

If using default deployment methodology (via `fab deploy`):

Edit `conf/production.env` in your Cabot clone to include the plugin and (optionally) a version number:

    CABOT_PLUGINS_ENABLED=cabot_alert_hipchat>=1.7.1,...,<other plugins>

Run `fab deploy -H ubuntu@yourserver.example.com` (see [http://cabotapp.com/qs/quickstart.html](http://cabotapp.com/qs/quickstart.html) for more information).

The `CABOT_PLUGINS_ENABLED` environment variable triggers both installation of the plugin (via [Cabot's `setup.py` file](https://github.com/arachnys/cabot/blob/fc33c9859a6c249f8821c88eb8506ebcad645a50/setup.py#L6)) and inclusion in `INSTALLED_APPS`.