# 🚀 Gemini MLOps Pipeline

This is an automated **End-to-End MLOps System** that uses the Google Gemini AI ecosystem to classify data. It features robust error handling, infrastructure automation, and workflow orchestration.

## 🛠️ Technical Stack
* **AI Engine:** Google Gemini SDK (1.5 Flash / 2.0)
* **Orchestrator:** Prefect 3.0 (Workflow Management)
* **Infrastructure:** Terraform & Docker
* **Automation:** PowerShell & Python

---

## 🚀 Execution Guide

### **LinkedIn Automation Bot** 🤖
Automated LinkedIn posting for MLOps projects using GitHub Actions.

#### **Setup Instructions**

1.  **Environment Variables**: Create `.env` file or set GitHub Secrets:
    ```env
    LINKEDIN_ACCESS_TOKEN=your_token
    LINKEDIN_PERSON_URN=your_urn
    GEMINI_API_KEY=your_gemini_key
    LINKEDIN_CLIENT_ID=your_client_id
    LINKEDIN_CLIENT_SECRET=your_client_secret
    GITHUB_REPO_URL=https://github.com/yourusername/repo
    ```

2.  **GitHub Secrets**: Add these secrets in GitHub Repository Settings:
    *   `LINKEDIN_ACCESS_TOKEN`
    *   `LINKEDIN_PERSON_URN`
    *   `GEMINI_API_KEY`
    *   `LINKEDIN_CLIENT_ID`
    *   `LINKEDIN_CLIENT_SECRET`

3.  **Local Testing**:
    ```bash
    pip install -r requirements.txt
    python test_bot.py
    python main.py
    ```

4.  **Schedule**: Posts daily at **9:00 AM UTC** (2:30 PM IST). Manual trigger available in GitHub Actions.

### **Quick Start**
To run the full pipeline, execute the PowerShell script in the root directory:
```powershell
.\quick_start.ps1
```

### 👩💻 Developed By
**[Bollinkala]** *Aspiring Cloud Engineer | B.Tech Student AI & ML*
