# ASPICE Audit — Full Stack Recommendation System (SWE.1–SWE.6)

ASPICE Audit is a full-stack web application that supports **continuous and automated assessment of Automotive SPICE (ASPICE)**, with a focus on the **Software Engineering process group SWE.1–SWE.6**.  
The system uses a **question-based evaluation approach** and an **AI-driven recommendation engine** to ask the most relevant questions to the most relevant stakeholders, per development cycle or software release.

---

## What This Application Does

### Continuous ASPICE SWE Assessment
Automotive SPICE is typically applied through periodic audits. This application aims to make ASPICE usable during daily development by enabling continuous monitoring of SWE processes:

- **SWE.1** — Software Requirements Analysis  
- **SWE.2** — Software Architectural Design  
- **SWE.3** — Software Detailed Design & Unit Construction  
- **SWE.4** — Software Unit Verification  
- **SWE.5** — Software Integration & Component Verification  
- **SWE.6** — Software Verification  

### Question Bank + Intelligent Question Selection
The application maintains a structured **question database** derived from ASPICE base practices and auditor expectations. Instead of asking long checklists, the system selects only a small set of high-impact questions per cycle using:

- Reinforcement Learning / **Contextual Multi-Armed Bandits (CMAB)**
- Weighted questions and scored answers
- Role-based context (stakeholder role, project phase, release scope)

### Results Dashboard
After stakeholders answer the selected questions, the system computes scores and generates a **process weakness classification** (e.g., Good / Medium / Bad) for SWE.1–SWE.6.  
The dashboard provides visibility into process weaknesses early, before defects appear late in testing or as defect tickets.

---

## Technology Stack and Features

- ⚡ **FastAPI** for the Python backend API  
  - 🧰 **SQLModel / SQLAlchemy** for database interaction (ORM)  
  - 🔍 **Pydantic** for validation and settings  
  - 💾 **PostgreSQL** (or MySQL if configured) as the database  
- 🚀 **React** for the frontend  
  - TypeScript, hooks, Vite  
  - Tailwind CSS + component UI library  
  - Role-based UI for different stakeholders  
- 🤖 **AI Recommendation Engine**  
  - Reinforcement Learning: **Contextual Multi-Armed Bandits (CMAB)**  
  - Question selection strategy per stakeholder context  
- 🔒 JWT Authentication + user roles  
  - Admin (manage question bank, weights, roles)  
  - Stakeholders (answer questions)  
  - Supervisor/Auditor view (review results)  
- 🐋 Docker Compose for local development and deployment  
- ✅ Tests (backend + frontend E2E if enabled)

---

## User Roles and Workflow

### Stakeholders (Answering Flow)
1. Stakeholder logs in  
2. System identifies their role/context  
3. AI selects a small set of questions (one-by-one flow)  
4. Stakeholder answers  
5. System calculates SWE.1–SWE.6 process weakness classification  
6. Stakeholder sees feedback and trends (if allowed by role)

### Admin (Configuration Flow)
- Manage question bank (SWE mapping, weights, answer options)  
- Manage stakeholder roles  
- View system-wide metrics and model performance

---

## How To Use It

Clone the repository:

```bash
git clone <your-repo-url> aspice-audit
cd aspice-audit