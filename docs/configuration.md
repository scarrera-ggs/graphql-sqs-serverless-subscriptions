# Configuration

This document defines the configuration parameters used in a deployment configuration file.

> :exclamation: There are some **default parameters** that should not be modified unless specified by the client, and some **manually inputted parameters** that **must** be filled by the deployment operator.

## Required Parameters

- `stack_name`:

  - **DESCRIPTION:** The name of the stack that will be deployed on AWS Cloudformation.
  - **VALUE:** _(suggestion)_ `<project-name>`.

- `s3_prefix`:

  - **DESCRIPTION:** The name of the S3 bucket where the lambda layer and lambda code will be stored.
  - **VALUE:** _(suggestion)_ `<project-name>`.

- `ConcertoRootUrl`:

  - **DESCRIPTION:** Concerto instance root url associated with this deployment.
  - **VALUE:** `https://<concerto_instance_name>.enbala-engine.com`.

## Default Parameters

- `ConcertoQueryTimeoutInSeconds`:

  - **DESCRIPTION:** Maximum waiting time in seconds to get response from Concerto.
  - **VALUE:** 30.

- `ConcertoApiWorkers`:

  - **DESCRIPTION:** Number of workers (threads) that will issue requests to Concerto.
  - **VALUE:** 10.

- `ConcertoApiMaxRetryAttempts`:

  - **DESCRIPTION:** Number of automatic retries if a request to Concerto API fails.
  - **VALUE:** 3.

- `ConcertoApiMaxRequestsPerPeriod`:

  - **DESCRIPTION:** Max requests per second that Concerto API allows.
  - **VALUE:** 25.

- `ConcertoTokenRotationSchedule`:

  - **DESCRIPTION:** AWS Event Bridge scheduler that triggers `ConcertoTokenRotationSchedule` lambda to update Concerto API access token.
  - **VALUE:** rate(30 minutes).

- `AssetLifecycleSubscriptionManagerSchedule`:

  - **DESCRIPTION:** AWS Event Bridge scheduler that triggers `AssetLifecycleSubscriptionManagerSchedule` lambda to update Asset Subscription User credentials.
  - **VALUE:** rate(30 minutes).
