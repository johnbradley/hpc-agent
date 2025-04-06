# HPC Agent
A website that provides a powerful chat interface for working in a HPC(High-performance Computing) Cluster.

## Requirements
- Python 3.10 or higher
- ANTHROPIC API Key

## Setup

### Install
To install directly from GitHub:
```bash
pip install git+https://github.com/johnbradley/hpc-agent.git
```

### Setup .env
Create a `.env` file in your project directory with the following content:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### Configure Environment

Create a `.env` file in your project directory:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Anthropic API key. The application will automatically load this file at startup.

> **Note:** If you don't have an API key yet, you can generate one at [Anthropic's Console](https://console.anthropic.com/settings/keys).

### Run
To run the HPC Agent, you can use the following command:

```bash
python -m hpc_agent
```

This will start the web server locally. By default, it will be accessible at `http://127.0.0.1:7860.

Once the server is running, open your web browser and navigate to the URL to access the chat interface.
