import streamlit as st
import requests
import time
from datetime import datetime
import os
from github import Github
import json

st.set_page_config(page_title="GitHub Actions Monitor", layout="wide")

# Custom CSS similar to the original app
st.markdown("""
<style>
@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}
@keyframes letterAppear {
    from { 
        opacity: 0;
        transform: translateX(50px);
    }
    to { 
        opacity: 1;
        transform: translateX(0);
    }
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
}
.floating-circle {
    width: 50px;
    height: 50px;
    background-color: #3498db;
    border-radius: 50%;
    margin: 20px auto;
    animation: float 3s ease-in-out infinite, pulse 2s ease-in-out infinite;
}
.letter {
    display: inline-block;
    animation: letterAppear 0.5s forwards;
    opacity: 0;
}
.status-badge {
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
}
.status-success { background-color: #28a745; color: white; }
.status-failure { background-color: #dc3545; color: white; }
.status-pending { background-color: #ffc107; color: black; }
</style>
""", unsafe_allow_html=True)

# Title with animation
st.markdown("""
    <h1 style='text-align: center; font-weight: bold;'>
        <span style='color: #FF9933;'>
            <span class="letter">G</span><span class="letter">i</span><span class="letter">t</span>
            <span class="letter">H</span><span class="letter">u</span><span class="letter">b</span>
        </span> 
        <span style='color: #138808;'>
            <span class="letter">A</span><span class="letter">c</span><span class="letter">t</span><span class="letter">i</span><span class="letter">o</span><span class="letter">n</span><span class="letter">s</span>
        </span>
    </h1>
    """, unsafe_allow_html=True)

def init_session_state():
    if 'github_token' not in st.session_state:
        st.session_state.github_token = ""
    if 'selected_repo' not in st.session_state:
        st.session_state.selected_repo = None
    if 'workflows' not in st.session_state:
        st.session_state.workflows = []
    if 'workflow_runs' not in st.session_state:
        st.session_state.workflow_runs = []

init_session_state()

def get_workflow_status_badge(status):
    if status == "completed":
        return "status-success"
    elif status == "failure":
        return "status-failure"
    else:
        return "status-pending"

def format_datetime(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

def get_repos(token):
    try:
        g = Github(token)
        return [repo.full_name for repo in g.get_user().get_repos()]
    except Exception as e:
        st.error(f"Error fetching repositories: {str(e)}")
        return []

def get_workflows(token, repo_name):
    try:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(
            f"https://api.github.com/repos/{repo_name}/actions/workflows",
            headers=headers
        )
        response.raise_for_status()
        return response.json()["workflows"]
    except Exception as e:
        st.error(f"Error fetching workflows: {str(e)}")
        return []

def get_workflow_runs(token, repo_name, workflow_id):
    try:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(
            f"https://api.github.com/repos/{repo_name}/actions/workflows/{workflow_id}/runs",
            headers=headers
        )
        response.raise_for_status()
        return response.json()["workflow_runs"]
    except Exception as e:
        st.error(f"Error fetching workflow runs: {str(e)}")
        return []

def trigger_workflow(token, repo_name, workflow_id):
    try:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.post(
            f"https://api.github.com/repos/{repo_name}/actions/workflows/{workflow_id}/dispatches",
            headers=headers,
            json={"ref": "main"}
        )
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Error triggering workflow: {str(e)}")
        return False

# GitHub token input
github_token = st.text_input(
    "GitHub Personal Access Token",
    type="password",
    value=st.session_state.github_token,
    help="Enter your GitHub Personal Access Token with workflow permissions"
)

if github_token:
    st.session_state.github_token = github_token
    repos = get_repos(github_token)
    
    # Repository selection
    selected_repo = st.selectbox(
        "Select Repository",
        options=repos,
        index=repos.index(st.session_state.selected_repo) if st.session_state.selected_repo in repos else 0
    )
    
    if selected_repo:
        st.session_state.selected_repo = selected_repo
        workflows = get_workflows(github_token, selected_repo)
        
        # Display workflows
        st.markdown("### Available Workflows")
        
        for workflow in workflows:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{workflow['name']}**")
            
            with col2:
                if st.button(f"View Runs", key=f"view_{workflow['id']}"):
                    st.session_state.workflow_runs = get_workflow_runs(
                        github_token,
                        selected_repo,
                        workflow['id']
                    )
            
            with col3:
                if st.button(f"Trigger", key=f"trigger_{workflow['id']}"):
                    if trigger_workflow(github_token, selected_repo, workflow['id']):
                        st.success("Workflow triggered successfully!")
                        time.sleep(2)
                        st.session_state.workflow_runs = get_workflow_runs(
                            github_token,
                            selected_repo,
                            workflow['id']
                        )

        # Display workflow runs
        if st.session_state.workflow_runs:
            st.markdown("### Recent Workflow Runs")
            for run in st.session_state.workflow_runs[:5]:  # Show last 5 runs
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"Run #{run['run_number']}")
                        st.write(f"Triggered by: {run['triggering_actor']['login']}")
                    
                    with col2:
                        st.write(f"Started: {format_datetime(run['created_at'])}")
                        if run['updated_at']:
                            st.write(f"Updated: {format_datetime(run['updated_at'])}")
                    
                    with col3:
                        status_class = get_workflow_status_badge(run['status'])
                        st.markdown(
                            f"<span class='status-badge {status_class}'>{run['status'].upper()}</span>",
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("---")

        # Auto-refresh button
        if st.button("Refresh Status"):
            if st.session_state.workflow_runs:
                workflow_id = st.session_state.workflow_runs[0]['workflow_id']
                st.session_state.workflow_runs = get_workflow_runs(
                    github_token,
                    selected_repo,
                    workflow_id
                )
                st.experimental_rerun()

else:
    st.info("Please enter your GitHub Personal Access Token to get started.")
    st.markdown("""
    To create a Personal Access Token:
    1. Go to GitHub Settings
    2. Select Developer Settings
    3. Navigate to Personal Access Tokens
    4. Generate a new token with 'workflow' and 'repo' permissions
    """)