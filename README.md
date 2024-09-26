# kube-debug-tracker

`kube-debug-tracker` is a Python-based tool designed to assist in tracking and documenting Kubernetes debugging sessions. It captures Kubernetes commands executed during debugging, logs their output, and creates structured entries in Notion, helping developers keep a detailed history of debugging activities.

## Features

- Track and document Kubernetes debugging processes.
- Capture all Kubernetes-related commands and their output from your terminal's history.
- Automatically log the debugging session, including the date and time, in a Notion page.
- Supports both `zsh` and `bash` history.
- Automatically splits large outputs to comply with Notion API limits.
- Appends commands and their output as numbered list items in Notion.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Artiach/kube-debug-tracker.git
    cd kube-debug-tracker
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### Notion Integration

1. Create a Notion integration and obtain your **Notion API Token**:
   - Go to [Notion Integrations](https://www.notion.so/my-integrations) and create a new integration.
   - Copy the **API Token** from the integration you just created.

2. Share your target Notion page or database with the integration:
   - Open the Notion page/database you want to log your debugging session to.
   - Click on "Share" and invite your integration using its name.

3. Create a `.env` file in the root of the project with the following environment variables:

    ```bash
    NOTION_API_TOKEN=your_notion_api_token
    NOTION_PAGE_ID=your_notion_page_id
    ```

### Shell History Setup

By default, `kube-debug-tracker` uses the `zsh` history file. If you're using `bash`, you can specify that with a flag when starting the debugging session.

## Usage

### Start a Debugging Session

To start tracking your Kubernetes commands, run the following command:

```bash
python3 cli.py --start-debugging
```


This command will:

    Create a new page in Notion with the current date and time.
    Start logging Kubernetes-related commands from your terminal history.

###End a Debugging Session

To stop the tracking and finalize the session, run:

```bash
python3 cli.py --end-debugging

```

This command will:

- Create a new page in Notion with the current date and time.
- Start logging Kubernetes-related commands from your terminal history.

## End a Debugging Session

To stop the tracking and finalize the session, run:

```bash
python3 cli.py --end-debugging

```

This will stop tracking and push the remaining commands and their outputs to the Notion page.

### Example

```bash
# Start debugging
python3 cli.py --start-debugging

# Run some Kubernetes commands
kubectl get pods
kubectl describe pod my-pod

# End debugging
python3 cli.py --end-debugging
```

This will create a numbered list in Notion like:

yaml

1. Command: kubectl get pods
    Output:
    pod-1   Running
    pod-2   Pending

2. Command: kubectl describe pod my-pod
    Output:
    Name: my-pod
    Namespace: default
    ...

Advanced Usage
Switching Between zsh and bash

By default, kube-debug-tracker reads the history from zsh. To switch to bash, use the --bash flag when starting the debugging session:

```bash

python3 cli.py --start-debugging --bash
```