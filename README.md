# Me service spike

Eventual production goals:

* Provide super-low latency (< 100 ms), high-priority information about a user to client apps.
* Reads the SSO cookie and returns user information (e.g. UUID, name), in addition to returning country information.
* Returns information from a DynamoDB global table -- apps (through a controlled mechanism) can deposit small sets of high-priority information there to be included in the info returned to the client (e.g. Accounts could place faculty verification status there, reading progress could put the last read location for each book, etc)
* Bundling information from multiple services in one request should further reduce latency
* Replaces `/api/user` on Accounts

Spike goals:

* Make a Lambda@Edge service that reads dev SSO cookies and returns user UUID, country code, and some information from a DynamoDB table (the first step towards me.openstax.org)
* Make a 2nd distribution on a different domain that references a pinned version of the me lambda function (so that later other sites like openstax.org can proxy me.openstax.org at openstax.org/me to avoid an extra SSL handshake to me.openstax.org, which can add 250-400 ms)

Production Todos:

* Global replication of parameter store secrets to all regions; have lambda function pick closest region to retrieve it (reduce latency); write a script that manages these secrets across regions; can also help us with cycling accounts secrets without interruption
* Monitor parameter store requests/sec under load.  Free gives us 40 requests/sec.  Could switch to 1000 req/sec but [we'd pay](https://aws.amazon.com/systems-manager/pricing/).  If there are issues, consider baking the Accounts secrets directly into the uploaded lambdas since they really aren't all that secret.


Reading

* [About XRay Traces](https://blog.newrelic.com/engineering/lambda-functions-xray-traces-custom-serverless-metrics/)
