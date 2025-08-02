# 🏥 MedCall

MedCall is a healthcare-first AI assistant designed to triage patients, log critical symptom data, and escalate emergencies. It leverages IBM’s **Agentic AI** through **Watsonx**, integrated into Slack for real-time, accessible care guidance.

---

## Features

- **Slack Integration** – Users interact with the MedCall bot in Slack.
- **Symptom Checker Agent** – Assesses patient-reported symptoms and offers initial guidance.
- **Patient Logger Agent** – Logs user-provided health issues and updates the session history.
- **Emergency Escalator Agent** – Identifies critical situations and recommends emergency care.
- **In-Memory Conversation History** – Maintains full agent context between interactions.
- **Slack Event Verification** – Securely verifies all incoming Slack events using signing secrets.

---

## Architecture

```
Slack → Node.js Middleware → FastAPI Backend → IBM Watsonx Agents
```

### Slack (Frontend)
- Captures user messages
- Verifies event authenticity
- Sends user messages to the backend via HTTP

### Node.js Slack Bot
- Middleware to interface with Slack events
- Forwards user input to FastAPI `/api/analyze`
- Posts back AI-generated responses

### FastAPI (Backend)
- Receives messages and Slack User ID
- Maintains in-memory message history per user
- Routes message chain through:
  1. **Symptom Checker**
  2. **Patient Logger**
  3. **Emergency Escalator**
- Returns the final agent response

### IBM Agentic AI Agents

| Agent               | Description                                                    |
|---------------------|----------------------------------------------------------------|
| `Symptom Checker`   | Analyzes natural language input for medical symptoms           |
| `Patient Logger`    | Records user history and context                               |
| `Emergency Escalator` | Escalates to emergency if risk detected                      |

---

## Technologies Used

| Stack       | Tool                        |
|-------------|-----------------------------|
| Language    | Python (FastAPI), Node.js   |
| AI          | IBM Watsonx Agent Lab, Orchestrate       |
| Messaging   | Slack API                   |
| HTTP        | Axios                       |
| Deployment  | Localhost (dev), IBM Cloud (prod) |

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/medcall.git
cd medcall
```

### 2. Slack Bot Setup

- Create a bot at [api.slack.com/apps](https://api.slack.com/apps)
- Enable:
  - `event:message.im`
  - `chat:write`
- Get your Slack **Bot Token** and **Signing Secret**

### 3. Backend Environment Setup

Create `backend/.env`:

```env
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_SPACE_ID=your_space_id
WATSONX_SERVICE_URL=https://eu-de.ml.cloud.ibm.com
WATSONX_DEPLOYMENT_ID_SYMPTOM=...
WATSONX_DEPLOYMENT_ID_LOGGER=...
WATSONX_DEPLOYMENT_ID_ESCALATOR=...
```

Install dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run FastAPI server:

```bash
uvicorn main:app --reload
```

### 4. Slack Bot Server Setup

Create `slack-bot/.env`:

```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=your-signing-secret
BACKEND_URL=http://localhost:8000/api/analyze
```

Install dependencies:

```bash
cd slack-bot
npm install
npm run dev
```

---

## Example Agent Flow

1. User sends: `I have chest pain and feel dizzy`
2. Backend stores message and routes to **Symptom Checker**
3. If risky symptoms detected, **Emergency Escalator** provides emergency instructions
4. Final response is sent back to Slack

---

## Testing

Send a message directly to your bot in Slack:

```
/dm @MedCall I’m feeling lightheaded and short of breath
```

Expected:
- Guidance from Symptom Checker
- Record in Logger
- Emergency escalation if needed

---

## 🔒 Security

- Slack requests are verified using `x-slack-signature` and `x-slack-request-timestamp`
- IBM API Keys are kept secure via `.env`

---

## 📌 Future Roadmap

- [✓] Agent chaining via memory graphs
- [ ] Integration with Electronic Health Records (EHR)
- [ ] SMS fallback via Twilio
- [ ] Persistent database logging
- [ ] Multilingual agent support

---

## 👨‍⚕️ Maintainers

- **Robert Odhiambo** – Project Lead

---

## 📄 License

MIT License. See `LICENSE` file.
