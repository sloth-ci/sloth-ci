# Validators

To run actions, the app must receive some sort of trigger request, e.g., a push notification from GitHub. The app checks all incoming requests, and only the ones that pass the check trigger actions. The requests usually contain data that should be passed to the actions, i.e., branch name, so the app must extract the data after the check.

In Sloth  CI, a source of trigger requests is called *provider*; e.g., GitHub, Bitbucket, and GitLab are providers. Each provider uses its own request format and thus requires its own validation and data extraction routine.

**Validator** implements request checking and data extraction for a particular provider. To add support of a new provider to Sloth CI, we just create a corresponding validator.


## Bitbucket


## GitHub


## GitLab
