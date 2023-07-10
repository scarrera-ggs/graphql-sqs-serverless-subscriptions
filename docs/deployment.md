# Deployment instructions

## Before deploying the project

### Install rtx

```bash
brew install jdxcode/tap/rtx
```

After `rtx` is installed open your shell configuration file

```bash
vim ~/.zshrc
```

Add the following lines to the file:

```text
eval "$(rtx activate zsh)"
export PATH="$HOME/.local/share/rtx/shims:$PATH"
export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"
```

For more information -> [install rtx](https://github.com/rtx-plugins/rtx-python).

### Install python

In your terminal go to your project directory make sure you have defined `.tool-versions` file in your project, then run:

```bash
rtx install python
```

### Install wheel

On the terminal, inside your project directory run:

```bash
pip install wheel
```

For more information -> [install wheel](https://wheel.readthedocs.io/en/stable/installing.html)

### Install poetry

On the terminal, inside your project directory run:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After `poetry` is installed open your shell configuration file

```bash
vim ~/.zshrc
```

Add the following lines to the file:

```text
export PATH=~/.local/bin:$PATH
```

For more information -> [install poetry](https://python-poetry.org/docs/#installation)

### Install sam cli

```bash
brew install aws/tap/aws-sam-cli
```

For more information -> [install sam-cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

### Setup AWS Account Credentials

Ensure you have setup a profile for the AWS CLI credentials to be used during the deployment. The deployment script sets the AWS_PROFILE environment variable as commonly found with other AWS tools.

### Gather Concerto Instance Username and Password

Follow the instruction to [Create a User in Concerto Instance](https://github.com/Enbala/infrastructure/wiki/Add-Remove-Users). Save the credentials (username, password).

### Configure Concerto Instance to accept GraphQL subscriptions

- Login into Concerto instance, run the following command:

```bash
ssh <concerto-instance>
```

- To execute programs as a super user, run the following command:

```bash
sudo su - vpp
```

- Start Elixir shell by running the following command:

```bash
vpp remote_console
```

- Run the following command to generate a new `aes_gcm_v1` value.

```bash
32 |> :crypto.strong_rand_bytes() |> Base.encode64()
```

:exclamation: Save the value generated from the previous command.

- Exit Elixir shell by pressing `control+c` **twice**.

- Edit VPP configuration by opening in the VIM editor the config file for the vpp.

```bash
vim /etc/vpp/config.toml
```

- Add/replace the following value under `[data_persist]` with the value gather for `aes_gcm_v1` in previous step.

```text
aes_gcm_v1 = "<aes_gcm_v1_value>"
```

- Save the config.toml file
- Restart vpp and make sure is running by running the following commands:

```bash
exit
```

```bash
sudo service vpp restart
```

```bash
enbala-info
```

- Finally, close SSH connection.

For more information -> [Configuring IEC104 Asset Adapter](https://github.com/Enbala/infrastructure/wiki/Adapter-Deployment-Process#configuring-iec104-asset-adapter) Or Connact @Woon.

## Project deployment

### Fill parameters on configuration toml file

Read [Configuration](configuration.md) documentation file to correctly fill the parameters for the project deployment.

> :information*source: Deployment configuration files should be created and submitted via Github PR_before* a deployment.

### Deploy project

```bash
bin/deploy --config <config_file_path> --profile <aws_profile> --region <aws_region>
```

## Post deployment configuration

### Set Concerto Credentials Secret

Login to the aws account console and locate the `ConcertoSecrets-<aws_resource_id>` resource under `AWS Secrets Manager`. Change the secret values with the values gathered from [Gather Concerto Instance Username and Password](#gather-concerto-instance-username-and-password) step.
