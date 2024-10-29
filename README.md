# GitHub Actions Monitor

A Streamlit-based web application to monitor and manage GitHub Actions workflows across repositories.

![GitHub Actions Monitor](https://img.shields.io/badge/GitHub-Actions%20Monitor-blue)

## Features

- Real-time monitoring of GitHub Actions workflows
- View workflow run history and status
- Trigger workflows manually
- Animated UI elements and status indicators
- Support for multiple repositories
- Secure token-based authentication

## Prerequisites

- Python 3.7+
- GitHub Personal Access Token with `workflow` and `repo` permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DMAP-saas-offer-frontend.git
cd DMAP-saas-offer-frontend
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Access the application in your browser at `http://localhost:8501`

3. Enter your GitHub Personal Access Token when prompted

4. Select a repository to view and manage its workflows

## Features Explained

### 1. Authentication
- Securely authenticate using GitHub Personal Access Token
- Token is stored in session state for the duration of use

### 2. Repository Management
- View all accessible repositories
- Select repositories to monitor workflows

### 3. Workflow Operations
- View all workflows in a selected repository
- Trigger workflows manually
- View recent workflow runs
- Monitor workflow status (Success/Failure/Pending)

### 4. Real-time Monitoring
- Refresh button to update workflow status
- View detailed run information including:
  - Run number
  - Triggering user
  - Start time
  - Last update time
  - Current status

## Security

- Personal Access Tokens are never stored permanently
- Tokens are transmitted securely using HTTPS
- Session-based token storage
- Password field masking for token input

## Technical Details

The application is built using:
- Streamlit - Web application framework
- PyGithub - GitHub API wrapper
- Requests - HTTP client library
- Custom CSS animations and styling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
