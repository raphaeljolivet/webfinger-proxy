# WARNING - EDIT

As per Mastodon developpers, this is not supported yet, and might cause issues on the servers.
Please don't use it on production servers until further notice.

See : https://github.com/tootsuite/mastodon/issues/2668


# Purpose 

Small Flask app for proxying your *.well-known/webfinger* to a remote host.

The purpose is to experiment custom domain handling for the ActivityPub / the Fediverse.

This app point any handle `<foo>@<your-domain.tld>` to `<foo>@<shared-instance.tld>`

# Setup 

Run this flask app on a custom local port :
```
> pip install -r requirements.txt
> export FLASK_RUN_PORT=nnnn
> flask run
```

(For real production deployment, consider using WGSI instead.)

Setup your web server as a proxy for  `/.well-known/`
See for instance [sample-apache.conf](sample-apache.conf)

# TODO

Restrict and configure the usage to some aliases only.
