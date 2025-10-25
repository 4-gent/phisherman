# Phisherman - AI Powered Phishing Training Tool

Please read this thoroughly to understand how to get things started. No matter what part you're working on, read the entire document. If you have any questions, reach out to Mj.

**Note:** Starting code has been made and commented for your reference to help you understand how communication between frontend and backend works and how the project works.

## Getting Started with Yarn Package Management

Yarn Package Manager allows you to install packages needed for web development, launch development servers, build projects into production builds, and much more.

**Note:** I highly recommend using Yarn for package management, but you are welcome to use npm or npx as well.

### How to Install Yarn Globally

#### Linux Environments

1. Update packages and install upgrades:
    ```bash
    sudo apt-get update && sudo apt-get full-upgrade -y
    ```
2. Install npm to install Yarn globally:
    ```bash
    sudo apt-get install npm -y
    sudo npm install -g yarn
    ```

#### macOS Environments

1. Install Homebrew (macOS package installer):
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. Install Yarn globally:
    ```bash
    brew install yarn
    ```

#### Windows Environments

1. If you do not have WSL/Bash on Windows (recommended), use the link below to install Yarn:
    [Yarn Installation for Windows](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable)

## Getting Started with Frontend

Frontend development is done using React.js, which combines JavaScript with HTML and CSS.

### Directory Structure
```
frontend
├── node_modules        # Installed npm packages (make sure .gitignore ignores this)
├── public              # Public assets (don’t worry about this)
└── src
    ├── components      # Reusable components (e.g., buttons)
    ├── styles          # CSS/styles and images
    ├── routes          # Additional webpages
    ├── main.js         # Home page JS file
    ├── App.js          # BrowserRouter routing file
    └── index.js        # Entry point (don’t modify this)
├── package.json        # Project blueprint and dependencies
└── .gitignore          # Ensure node_modules is ignored
```

### How to Get It Running

1. **`cd`** into the `frontend` folder.

2. Run **`yarn install`** (**`sudo yarn install`** on Unix-based systems) to download packages specified in `package.json`.

3. Start the development server by running **`yarn start`** (or **`sudo yarn start`**). The server will start at **`http://localhost:3000`**.

    - As you code and make updates, it will compile and show you runtime errors/changes as you develop.

**Note:** Remember to update the BrowserRouter in `App.js` to ensure the application recognizes the new page you create.

## Getting Started with Backend

The backend server will be handled with python websockets to send and receive instructions.

- `main.py` will be the main backend code (abstracting python files makes it easier to make modular).

### Directory Structure
```
backend
├── venv                  # Activate virtual python environment (make sure to activate this before starting to code)
└── mail                   # defensive directory
    ├── sender               # idr code here
        └── sender.py
└── phisher                   # offensive directory
    ├── agent               # dos code here
        └── agent.py
├── main.py               # main parent source code
├── Requirements.txt      # install the requirements AFTER initalizing the venv
└── .gitignore            # Ensure node_modules is ignored
```

### How to Get It Running

1. If you do not have Python and pip installed, install them first.

2. Initialize the virtual environment
    ```bash
    python3 (or python) -m venv venv
    source ./venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip3 (or pip) install -r Requirements.txt
    ```

3. Start the hermes server:
    ```bash
    python main.py

