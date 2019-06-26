from flask import Flask, request, render_template, url_for, redirect, session, Response
import json
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(20)

api_key = os.environ.get('PD_API_KEY') or "Set the PD_API_KEY environment variable to a PagerDuty API key"
from_email = os.environ.get('PD_FROM_EMAIL') or "Set the PD_FROM_EMAIL environment variable to a PagerDuty login email"

@app.route('/mirrorincident', methods=["post"])
def mirrorincident():
	headers = {
		'Authorization': f"Token token={api_key}",
		'Accept': 'application/vnd.pagerduty+json;version=2',
		'Content-Type': 'application/json',
		'From': from_email
	}

	service_id = request.args.get('service_id')
	ep_id = request.args.get('ep_id')
	urgency = request.args.get('urgency') or 'low'
	conf_number = request.args.get('conf_number')
	conf_url = request.args.get('conf_url')
	req_body = request.json

	for message in req_body.get("messages"):
		if message.get("event") == "incident.custom":
			title = message["incident"]["title"]
			description = message["incident"]["description"]
			post_body = {
				"incident": {
					"type": "incident",
					"title": title,
					"service": {
						"id": service_id,
						"type": "service_reference"
					},
					"urgency": urgency,
					"body": {
						"type": "incident_body",
						"details": description
					},
					"conference_bridge": {
						"conference_number": conf_number,
						"conference_url": conf_url
					}
				}
			}
			if ep_id:
				post_body["escalation_policy"] = {
					"id": ep_id,
					"type": "escalation_policy_reference"
				}

			response = requests.post(url='https://api.pagerduty.com/incidents', headers=headers, json=post_body)
			if response.status_code > 299:
				print(f"Error {response.status_code}:")
				print(response.json())

	return "ok"
