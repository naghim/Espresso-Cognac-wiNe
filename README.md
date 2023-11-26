# (E)spresso (C)ognac wi(N)e

a.k.a. Sapientia-ECN Contest Submissions Downloader.

This repository contains a Python script that allows you to download all student submissions for a contest from an online judger system (website). This tool automates the process of fetching submissions, providing a convenient way to manage, analyze, and archive student entries.

## Requirements

- Python 3.x

- Required Python packages (install using `pip install -r requirements.txt`):

  - `requests`: Used for making HTTP requests to the judger system.

  - `beautifulsoup4`: A web scraping library for parsing HTML.

## Usage

**Step 1.** Clone the repository to your local machine:

`git clone https://github.com/naghim/Espresso-Cognac-wiNe.git`

**Step 2.** Navigate to the project directory:

`cd Espresso-Cognac-wiNe`

**Step 3.** Install the required packages:

`python -m pip install -r requirements.txt`

**Step 4.** Create a `users.json` file with the teams' judger system credentials and names. Use the following format:

```
[
  { "team": "Team 1", "username": "team1username", "password": "team1pwd" },
  { "team": "Team 2", "username": "team2username", "password": "team2pwd" },
  ...
  { "team": "Team N", "username": "teamNusername", "password": "teamNpwd" }
]
```

**Step 5.** Run the script:

`python download_submissions.py`
