# PDmirrorincident
Custom action to create a mirror incident with conf bridge info

## Summary
This is a Flask app that presents an /mirrorincident endpoint that can be the destination for a custom action. 

## Local Installation
Clone this repo. Then:
```
python3 -m venv venv                   # create a virtual environment
. venv/bin/activate                    # activate it
pip install -r requirements.txt        # install the dependencies
FLASK_DEBUG=true \
PD_API_KEY=<A_PD_API_KEY> \
PD_FROM_EMAIL=<A_PD_LOGIN_EMAIL> \
flask run             # run the app in flask with debug on
```

## Usage

Create a custom action in Pagerduty whose URL looks like this:

```
https://<HOSTNAME>/mirrorincident?service_id=<DESTINATION_SERVICE_ID>&conf_number=<CONF_BRIDGE_NUMBER>&conf_url=<CONF_BRIDGE_URL>
```

optionally you can add `ep_id=<ESCALATION_POLICY_ID>` and `urgency=<URGENCY>`
