# Phisherman Architecture Diagram

**Multi-agent system using Fetch.ai uAgents and Agentverse**

---

## System Architecture

```mermaid
graph TB
    subgraph "Frontend Application"
        UI[React UI]
        Quiz[Quiz Component<br/>WebSocket Client]
    end
    
    subgraph "Backend Proxy"
        Flask[Flask API<br/>Routes + Proxy]
    end
    
    subgraph "Agentverse Platform"
        AV[Agentverse<br/>Discovery & Hosting]
        Analytics[Rating & Analytics]
    end
    
    subgraph "Phisherman Agents"
        PM[Phish Master<br/>Orchestrator<br/>Port 8001]
        FP[Finance Phisher<br/>Domain Agent<br/>Port 8002]
        HP[Health Phisher<br/>Domain Agent<br/>Port 8003]
        PP[Personal Phisher<br/>Domain Agent<br/>Port 8004]
        PR[Phish Refiner<br/>Content Optimizer<br/>Port 8005]
        TA[Teacher Agent<br/>Educational Trainer<br/>Port 8006]
    end
    
    subgraph "Chat Protocol v0.3.0"
        CP[ChatMessage<br/>StartSessionContent<br/>TextContent<br/>EndSessionContent]
    end
    
    subgraph "Safety Layer"
        Refusal[Refusal Handler<br/>is_harmful_request]
        Sanitize[Template Sanitizer<br/>Placeholder URLs]
        Audit[Audit Logs<br/>backend/logs/]
    end
    
    UI --> Flask
    Quiz --> Flask
    Flask --> PM
    Flask --> TA
    
    PM -->|Orchestrates| FP
    PM -->|Orchestrates| HP
    PM -->|Orchestrates| PP
    PM -->|Routes| PR
    
    PM -.->|Registered| AV
    FP -.->|Registered| AV
    HP -.->|Registered| AV
    PP -.->|Registered| AV
    PR -.->|Registered| AV
    TA -.->|Registered| AV
    
    AV --> Analytics
    
    PM --> CP
    FP --> CP
    HP --> CP
    PP --> CP
    PR --> CP
    TA --> CP
    
    PM --> Refusal
    FP --> Refusal
    HP --> Refusal
    PP --> Refusal
    PR --> Refusal
    TA --> Refusal
    
    FP --> Sanitize
    HP --> Sanitize
    PP --> Sanitize
    PR --> Sanitize
    
    PM --> Audit
    FP --> Audit
    HP --> Audit
    PP --> Audit
    PR --> Audit
    TA --> Audit
    
    style PM fill:#ff6b6b
    style FP fill:#4ecdc4
    style HP fill:#45b7d1
    style PP fill:#96ceb4
    style PR fill:#ffeaa7
    style TA fill:#dda0dd
    style AV fill:#a29bfe
    style Refusal fill:#ff7675
    style Sanitize fill:#74b9ff
    style Audit fill:#fdcb6e
```

---

## Message Flow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Flask
    participant PM as Phish Master
    participant FP as Finance Phisher
    participant AV as Agentverse
    participant Quiz as Quiz UI
    
    User->>Flask: POST /api/campaign<br/>{template: "finance"}
    Flask->>PM: Orchestrate Flow
    PM->>AV: Discover Finance Phisher
    AV-->>PM: Finance Phisher Address
    PM->>FP: ChatMessage<br/>"generate finance template"
    FP->>FP: Check Refusal Handler
    FP->>FP: Generate Template<br/>(Sanitized)
    FP-->>PM: ChatMessage<br/>{sanitized_json}
    PM->>PM: Aggregate Response
    PM-->>Flask: Template JSON
    Flask-->>User: {success: true, template: {...}}
    
    Note over User,Quiz: Quiz Pipeline
    User->>Quiz: Start Quiz Session
    Quiz->>TA: WebSocket Connect
    TA->>TA: Load Lesson<br/>"suspicious_link"
    TA-->>Quiz: Question + Options
    User->>Quiz: Select Answer
    Quiz->>TA: Submit Answer
    TA->>TA: Evaluate Answer
    TA-->>Quiz: +10 (correct) or -10 (incorrect)
    Quiz->>Quiz: Update Scoreboard
```

---

## Agent Registration Flow

```mermaid
graph LR
    subgraph "Development"
        Code[Agent Code<br/>main.py]
        Config[Agentverse Config<br/>JSON]
    end
    
    subgraph "Registration"
        Reg[Agentverse Registration<br/>Name, Handle, Manifest]
        SEO[SEO Fields<br/>Tags, Capabilities]
        README[README Link<br/>Documentation]
    end
    
    subgraph "Discovery"
        ASI[ASI:One Search]
        Search[Tag Search<br/>phishing, cybersecurity]
        Chat[Chat Protocol<br/>v0.3.0]
    end
    
    Code --> Config
    Config --> Reg
    Reg --> SEO
    Reg --> README
    SEO --> ASI
    README --> ASI
    Reg --> Chat
    Chat --> Search
    Search --> ASI
```

---

## Safety Architecture

```mermaid
graph TB
    Request[User Request]
    
    Check{Refusal Handler<br/>is_harmful_request}
    
    Refuse[Refusal Response<br/>Audit Log]
    
    Generate[Template Generation]
    
    Sanitize[Sanitization Layer]
    
    Output[Sanitized Template<br/>Placeholder URLs<br/>Template Variables]
    
    Request --> Check
    Check -->|Harmful| Refuse
    Check -->|Safe| Generate
    Generate --> Sanitize
    Sanitize --> Output
    
    Refuse --> Audit[Audit Logs]
    Output --> Audit
    
    style Refuse fill:#ff7675
    style Sanitize fill:#74b9ff
    style Output fill:#00b894
    style Audit fill:#fdcb6e
```

---

## Technology Stack

```
┌─────────────────────────────────────────┐
│         Frontend (React)                │
│  - Quiz Component (WebSocket)          │
│  - Dashboard UI                        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Backend Proxy (Flask)              │
│  - /api/campaign (POST)                 │
│  - /api/completion (POST)              │
│  - Error Handling & Logging            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│     uAgents Framework                    │
│  - Agent(name="...")                    │
│  - Protocol()                           │
│  - ChatMessage handlers                 │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│   Chat Protocol v0.3.0                  │
│  - StartSessionContent                  │
│  - TextContent                          │
│  - EndSessionContent                    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Agentverse Platform                │
│  - Hosted Agents                        │
│  - Discovery & Search                   │
│  - Rating & Analytics                   │
└─────────────────────────────────────────┘
```

---

## Component Descriptions

### Orchestrator Layer
- **Phish Master**: Routes requests to domain agents, aggregates responses

### Domain Agents
- **Finance Phisher**: Banking, payment verification scenarios
- **Health Phisher**: Medical records, insurance scenarios
- **Personal Phisher**: Social media, password reset scenarios

### Specialized Agents
- **Phish Refiner**: Content optimization, urgency adjustment
- **Teacher Agent**: Educational lessons, quiz pipeline

### Infrastructure
- **Agentverse**: Discovery, hosting, analytics
- **Chat Protocol**: Standardized message format
- **Safety Layer**: Refusal handlers, sanitization, audit logs

---

## Key Design Principles

1. **Separation of Concerns**: Each agent has a single responsibility
2. **Protocol Compliance**: All agents use Chat Protocol v0.3.0
3. **Safety First**: Refusal paths, sanitized outputs, audit logs
4. **Interoperability**: Standard endpoints enable cross-agent communication
5. **Observability**: Comprehensive logging and analytics

---

**Diagram Export**: Use Mermaid Live Editor (https://mermaid.live) to render as PNG/SVG

