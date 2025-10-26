# 🎣 Phisherman - AI-Powered Phishing Training Platform

**Built for CalHacks 2025 - Fetch.ai Track**

Phisherman is an AI-powered cybersecurity training platform that generates safe, educational phishing emails using 5 specialized AI agents. The platform helps organizations train their employees to recognize and avoid phishing attacks through realistic, controlled training scenarios.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- Yarn package manager

### 1. Start All Agents (Mailbox Mode)
```bash
# Clone the repository
git clone https://github.com/raghavgautam/phisherman.git
cd phisherman

# Start all 5 AI agents
./start_all.sh
```

### 2. Start Frontend
```bash
cd frontend
yarn install
yarn start
```

### 3. Start Backend
```bash
cd backend
pip install -r Requirements.txt
python main.py
```

## 🤖 AI Agents Overview

Phisherman uses 5 specialized AI agents working together:

1. **Phish Master** (Orchestrator) - Coordinates all other agents
2. **Finance Phisher** - Generates financial phishing templates
3. **Health Phisher** - Creates healthcare phishing scenarios
4. **Personal Phisher** - Develops personal information phishing templates
5. **Phish Refiner** - Optimizes and improves phishing templates

## 🔧 Agentverse Registration

### Mailbox Configuration
All agents run in **mailbox mode** for Agentverse registration:

- **Chat Protocol v0.3.0** compatible
- **No blockchain registration** required
- **FastAPI-based** endpoints
- **Health check** endpoints for monitoring

### Registration Steps
1. **Start agents**: `./start_all.sh`
2. **Copy JSON configs** from `agentverse_configs/` folder
3. **Register on Agentverse** using the provided JSON files
4. **Test ASI:One discovery** through the platform

### Agent URLs
- Phish Master: `http://127.0.0.1:8001`
- Finance Phisher: `http://127.0.0.1:8002`
- Health Phisher: `http://127.0.0.1:8003`
- Personal Phisher: `http://127.0.0.1:8004`
- Phish Refiner: `http://127.0.0.1:8005`

### Endpoints for Each Agent
- `/health` - Health check
- `/agent_info` - Agent metadata for Agentverse
- `/chat` - Chat Protocol v0.3.0 messaging
- `/generate` - Phishing template generation

## 📁 Project Structure

```
phisherman/
├── backend/
│   ├── mail/sender/
│   │   ├── phish_master/          # Orchestrator agent
│   │   ├── finance_phisher/       # Financial phishing agent
│   │   ├── health_phisher/       # Healthcare phishing agent
│   │   ├── personal_phisher/     # Personal info phishing agent
│   │   ├── phish_refiner/        # Template refinement agent
│   │   └── mailbox_agent.py      # Mailbox mode implementation
│   ├── config.py                 # Backend configuration
│   ├── main.py                   # Flask backend server
│   └── Requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── routes/              # Page routes
│   │   └── styles/              # CSS styles
│   └── package.json             # Frontend dependencies
├── agentverse_configs/          # Agentverse registration JSON files
├── diagnostics/                 # Troubleshooting logs
├── tests/                       # Test results and samples
├── start_all.sh                # Start all agents script
└── README_AGENTVERSE.md        # Detailed registration guide
```

## 🛡️ Safety & Compliance

- **Educational Purpose Only**: All generated content is for cybersecurity training
- **Safe Templates**: No real phishing attacks are conducted
- **Clear Marking**: All content is clearly marked as training material
- **Controlled Environment**: Agents operate in secure, controlled conditions
- **Ethical AI**: Responsible AI practices for cybersecurity education

## 🧪 Testing & Verification

### Local Testing
```bash
# Test all agents
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8002/health
curl http://127.0.0.1:8003/health
curl http://127.0.0.1:8004/health
curl http://127.0.0.1:8005/health

# Test chat protocol
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Generate a financial phishing template"}'

# Test template generation
curl -X POST http://127.0.0.1:8002/generate \
  -H "Content-Type: application/json" \
  -d '{"domain": "finance", "urgency_level": 8}'
```

### Verification Results
- ✅ All agents responding
- ✅ Chat Protocol v0.3.0 working
- ✅ Template generation functional
- ✅ Inter-agent communication working
- ✅ Mailbox mode operational

## 🔗 Agentverse Integration

### Registration Files
- `agentverse_configs/phish_master_agentverse_config.json`
- `agentverse_configs/finance_phisher_agentverse_config.json`
- `agentverse_configs/health_phisher_agentverse_config.json`
- `agentverse_configs/personal_phisher_agentverse_config.json`
- `agentverse_configs/phish_refiner_agentverse_config.json`

### ASI:One Discovery
After registration, agents are discoverable through ASI:One with tags:
- `phishing`, `cybersecurity`, `training`
- `finance`, `healthcare`, `personal-info`
- `template-generation`, `agent-coordination`

## 🚨 Troubleshooting

### Common Issues
1. **Port conflicts**: Run `lsof -ti:8001,8002,8003,8004,8005 | xargs kill -9`
2. **Dependency issues**: Run `pip install -r backend/Requirements.txt`
3. **Agent registration fails**: Check `diagnostics/` folder for logs
4. **Public access needed**: Use ngrok (see `diagnostics/ngrok_fallback.txt`)

### Diagnostic Files
- `diagnostics/port_report.txt` - Port conflict resolution
- `diagnostics/dependency_fix.txt` - Dependency troubleshooting
- `diagnostics/mailbox_setup.txt` - Mailbox configuration
- `diagnostics/ngrok_fallback.txt` - Public access setup

## 📚 Documentation

- **Main README**: This file
- **Agentverse Guide**: `README_AGENTVERSE.md`
- **Configuration**: `config/disable_auto_funding.md`
- **Test Results**: `tests/run_log.txt`

## 🎯 Demo Script (60-90 seconds)

### For Judges/Demo:
1. **Show agent startup**: `./start_all.sh`
2. **Demonstrate health checks**: All 5 agents responding
3. **Show chat protocol**: Agent communication working
4. **Generate template**: Finance phishing template creation
5. **Show Agentverse configs**: Ready for registration
6. **Test ASI:One discovery**: Agents discoverable on platform

### Key Points to Highlight:
- **5 AI agents** working together
- **Mailbox mode** for Agentverse compatibility
- **Chat Protocol v0.3.0** compliance
- **Safe, educational** phishing training
- **ASI:One discovery** ready
- **Fetch.ai ecosystem** integration

## 🤝 Contributing

This project was built for CalHacks 2025 - Fetch.ai Track. For questions or contributions, please refer to the project repository.

## 📄 License

This project is for educational and demonstration purposes as part of CalHacks 2025.

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

