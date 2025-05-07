# Gitxplorer

A dark-themed Flask application to search for juicy information on GitHub using custom dorks. This tool enables users to select specific dorks (e.g., "Passwords", "API Keys") or provide their own custom keyword. Additionally, it supports searching within a specific repository and paginates results for enhanced usability.

## Features

- **Search with GitHub Dorks:** Use pre-defined dorks to search for sensitive information.
- **Custom Keyword Override:** Enable a custom keyword to override the dorks selections.
- **Repository Filter:** Optionally limit the search to a specific repository.
- **Pagination:** Initially fetch results from page 1. Load additional pages on demand.
- **Professional UI:** Modern, dark-themed UI layout with a sidebar for settings and a main panel for the search form and results.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ubaidahmed2803/Gitxplorer.git
   cd Gitxplorer```
2. **Create a Virtual Environment (optional but recommended):**

   ```bash
      python -m venv venv
      source venv/bin/activate   # On Windows: venv\Scripts\activate
   
3. **Install Dependencies:**

   ```bash
      pip install -r requirements.txt
   
4. **Configure GitHub Token:**
   Create a config.ini file in the root directory with the following content:

   ```bash
      [GitHub]
      TOKEN=
   
## Usage

1. **Run the application**

   ```bash
   python app.py

2. **Access the application**

   Open your browser and navigate to http://127.0.0.1:5000/.

3. **Perform a search**

   - Sidebar: Use the left panel to select or deselect GitHub dorks.
   - Main Form: Enter your GitHub token, and if desired, toggle "Enable Custom Keyword" to provide a search term that overrides the dorks. You can also provide a repository (optional).
   - Click "Start Search" to initiate the search.
  
4. **Pagination**

   - The initial search displays results from page 1.
   - If more pages are available, a "Load Next 5 Pages" button will be visible. Click this button to load additional results.
  




