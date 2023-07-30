# CI/CD Pipeline

The CI/CD Pipeline is configure for push/pull requests from the main or develop branch. Feel free to change it. The following environment varibles must added with your own ones in the ci-test.yml to make it run.

```bash
RUN_ID: aa806b4bc4044777a0a25d5b8a24d7d5
BUCKET_NAME: mlflow-tracking-remote
EXPERIMENT_ID: 29
```

The tests will run in GitHub Actions.
