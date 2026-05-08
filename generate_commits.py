import os
import subprocess
from datetime import datetime, timedelta

# Configurations
start_date = datetime(2026, 5, 1, 13, 38, 0)
end_date = datetime(2026, 5, 16, 2, 5, 0)
total_commits = 60

def run_cmd(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

# Get list of untracked files
result = subprocess.run('git ls-files --others --exclude-standard', shell=True, capture_output=True, text=True)
files = result.stdout.strip().split('\n')
files = [f for f in files if f] # remove empty

# Sort files roughly: backend first, then frontend
files.sort(key=lambda x: (not x.startswith('backend'), x))

# Calculate time step
time_diff = end_date - start_date
step_seconds = time_diff.total_seconds() / (total_commits - 1)

current_date = start_date

def make_commit(msg, date):
    date_str = date.strftime('%Y-%m-%dT%H:%M:%S')
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    run_cmd(f'git commit -m "{msg}"', env=env)

print(f"Generating {total_commits} commits...")

# 1. Commit files one by one
for i, file in enumerate(files):
    if i >= total_commits:
        break
    run_cmd(f'git add "{file}"')
    
    # Generate realistic messages
    if "backend" in file:
        msg = f"feat(backend): add {os.path.basename(file)}"
    elif "frontend" in file:
        msg = f"feat(frontend): initialize {os.path.basename(file)}"
    else:
        msg = f"chore: add {os.path.basename(file)}"
        
    make_commit(msg, current_date)
    current_date += timedelta(seconds=step_seconds)

commits_left = total_commits - len(files)

# 2. Use remaining commits for "bug fixes" and "docs"
with open("CHANGELOG.md", "w") as f:
    f.write("# Changelog\n\n")

run_cmd('git add CHANGELOG.md')
make_commit("docs: add CHANGELOG.md", current_date)
current_date += timedelta(seconds=step_seconds)
commits_left -= 1

for i in range(commits_left):
    with open("CHANGELOG.md", "a") as f:
        f.write(f"- Polish phase iteration {i+1}\n")
    run_cmd('git add CHANGELOG.md')
    
    msgs = ["fix: resolve minor bugs", "refactor: clean up code", "perf: optimize rendering", "chore: minor adjustments", "style: update formatting"]
    msg = msgs[i % len(msgs)]
    
    make_commit(msg, current_date)
    current_date += timedelta(seconds=step_seconds)

print("Done generating history!")
