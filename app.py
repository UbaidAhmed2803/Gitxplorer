import os
import math
import requests
import configparser
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Setup Flask
app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config["SESSION_TYPE"] = "filesystem"  # for larger session storage if needed

# GitHub Dorks List (used on the left sidebar)
DORKS = [
    "Passwords",
    "API Keys",
    "Database Credentials",
    "AWS Keys",
    "SSH Keys"
]

# Read and write GitHub token in config.ini
config = configparser.ConfigParser()
config.read("config.ini")

def save_github_token(token):
    """Save the GitHub token to config.ini"""
    config["GitHub"] = {"TOKEN": token}
    with open("config.ini", "w") as configfile:
        config.write(configfile)

def get_github_token():
    """Retrieve GitHub token from config.ini"""
    return config["GitHub"].get("TOKEN", "")

def github_search(query, token, page=1, per_page=5):
    """
    Perform GitHub search using the API with pagination.
    Returns a JSON object. Expected keys include "total_count" and "items".
    """
    headers = {"Authorization": f"token {token}"}
    params = {"q": query, "per_page": per_page, "page": page}
    try:
        response = requests.get("https://api.github.com/search/code", headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Homepage – Accept GitHub token, dork selection, and search settings.
    
    New Logic:
    • If the "Enable Custom Keyword" toggle is checked and the custom keyword field is non-empty,
      then override all dork selections and search only for the provided custom keyword.
    • Otherwise, use the selected dorks (or all dorks by default if none are selected).
    
    For each query, page 1 is fetched along with information about total pages.
    The search state (including all queries and their current results) are stored in the session.
    """
    if request.method == "POST":
        token = request.form.get("github_token").strip()
        enable_keyword = request.form.get("enableKeyword")  # Checkbox state (if present, its value will be "on")
        custom_keyword = request.form.get("search_term", "").strip() if enable_keyword else ""
        repo = request.form.get("repo", "").strip()
        selected_dorks = request.form.getlist("dorks")

        if token:
            save_github_token(token)

        per_page = 5
        search_state = {"queries": [], "results": {}, "token": token, "per_page": per_page}

        # If a custom keyword is provided and enabled, override everything.
        if enable_keyword and custom_keyword:
            query = custom_keyword
            if repo:
                query = f"repo:{repo} {query}"
            result = github_search(query, token, page=1, per_page=per_page)
            total_count = result.get("total_count", 0)
            pages_count = math.ceil(total_count / per_page) if total_count else 0
            query_state = {
                "query": query,
                "current_page": 1,   # we just fetched page 1
                "total_count": total_count,
                "pages_count": pages_count
            }
            search_state["queries"].append(query_state)
            # Store the initial page results for this query.
            search_state["results"][query] = result.get("items", [])
        else:
            # Otherwise, use the dork selections. If none are selected, use all available dorks.
            if not selected_dorks:
                selected_dorks = DORKS

            for dork in selected_dorks:
                query = dork
                if repo:
                    query = f"repo:{repo} {query}"
                result = github_search(query, token, page=1, per_page=per_page)
                total_count = result.get("total_count", 0)
                pages_count = math.ceil(total_count / per_page) if total_count else 0
                query_state = {
                    "query": query,
                    "current_page": 1,
                    "total_count": total_count,
                    "pages_count": pages_count
                }
                search_state["queries"].append(query_state)
                search_state["results"][query] = result.get("items", [])

        # Save the search state in session so we can paginate later.
        session["search_state"] = search_state
        return render_template("results.html", search_state=search_state)

    # For GET requests, simply render the index page.
    return render_template("index.html", dorks=DORKS, token=get_github_token())

@app.route("/paginate", methods=["POST"])
def paginate():
    """
    This route is called when the user clicks "Load Next 5 Pages".
    For each query in our search_state, if there are additional pages available,
    we fetch the next 5 pages (or as many as remain) and append the items to the existing results.
    Then we update the current page number.
    """
    search_state = session.get("search_state", None)
    if not search_state:
        flash("No search session found. Please perform a search first.", "warning")
        return redirect(url_for("index"))

    token = search_state["token"]
    per_page = search_state["per_page"]

    # For each query, fetch next pages if available.
    for query_state in search_state["queries"]:
        current_page = query_state["current_page"]
        pages_count = query_state["pages_count"]
        if current_page < pages_count:
            # Determine how many pages to fetch this time (up to 5).
            next_pages_to_fetch = min(5, pages_count - current_page)
            for i in range(1, next_pages_to_fetch + 1):
                page_to_fetch = current_page + i
                result = github_search(query_state["query"], token, page=page_to_fetch, per_page=per_page)
                items = result.get("items", [])
                search_state["results"][query_state["query"]].extend(items)
            # Update the current_page after fetching additional pages.
            query_state["current_page"] = current_page + next_pages_to_fetch

    # Save the updated state back into session.
    session["search_state"] = search_state

    return render_template("results.html", search_state=search_state)

if __name__ == "__main__":
    app.run(debug=True)
