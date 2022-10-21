# Instructions for integrating Slack and Airflow

Follow this for good instructions on the steps required to:

1) Create a Slack app
2) Confirm the settings required to allow comms to the app using the API
https://towardsdatascience.com/integrating-docker-airflow-with-slack-to-get-daily-reporting-c462e7c8828a

### Re: 'Step 4: DAG Definition' and the webhook_token
(lifted from: https://www.reddit.com/r/dataengineering/comments/k67u5d/not_getting_slack_notifications_when_dags_fail/gv8ausz/)

The examples often don't really say what part of the webhook token is required in the below:

    `post_daily_forecast = SlackWebhookOperator(
        task_id='post_daily_forecast',
        http_conn_id='slack_connection',
        webhook_token=os.environ['slack_webhook_url'],
        message=get_daily_forecast(),
        channel='#daily-weather-feed'`

So the key thing to callout:

* The webbook will look like:
`https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`
* (important) where the token portion of it will be `T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`


### Re: 'Setting up your Slack connection on Airflow'

Instead, follow the instructions below (lifted from here: https://medium.com/datareply/integrating-slack-alerts-in-airflow-c9dcd155105)

1) Go to Admin > Connections
2) Create a new Connection

Create an Airflow connection for Slack with HTTP connection and the part after https://hooks.slack.com/services should go under password:

Conn Type: HTTP
Host: https://hooks.slack.com/services
Password: /T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX

- Hit Create and fill the fields accordingly.
- For the Slack connection (important), use the following details:

conn_id = slack_connection (string value)
host = your webhook URL

Also for reference: https://stackoverflow.com/questions/52054427/how-to-integrate-apache-airflow-with-slack
