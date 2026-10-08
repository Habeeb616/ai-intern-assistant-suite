from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import os
import datetime

app = FastAPI(title="Enterprise RAG AI Engine")

class QueryRequest(BaseModel):
    question: str

class LeaveRequest(BaseModel):
    shift_start_time: str  # Format: HH:MM (24hr)
    report_time: str       # Format: HH:MM (24hr)

STIPEND_BALANCE = 15000
LOG_FILE = "transaction_history.txt"
CSV_FILE = "transaction_history.csv"

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html>
        <head>
            <title>AlphaTech Solutions - Complete Intern Suite</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; background-color: #f4f6f9; }}
                .card {{ background: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 25px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                input[type="text"], input[type="time"] {{ padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; }}
                input[type="text"] {{ width: 75%; }}
                button {{ padding: 10px 20px; font-size: 16px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }}
                button:hover {{ background-color: #0056b3; }}
                .claim-btn {{ background-color: #28a745; width: 100%; padding: 12px; font-size: 18px; margin-top: 10px; }}
                .claim-btn:hover {{ background-color: #218838; }}
                .verify-btn {{ background-color: #17a2b8; }}
                .verify-btn:hover {{ background-color: #138496; }}
                .download-btn {{ background-color: #6c757d; font-size: 12px; padding: 5px 10px; margin-left: 10px; }}
                .download-btn:hover {{ background-color: #5a6268; }}
                #result, #claim-status, #leave-status {{ margin-top: 15px; padding: 15px; background: #f8f9fa; border-left: 5px solid #007bff; font-weight: bold; border-radius: 0 4px 4px 0; }}
                #claim-status {{ border-left-color: #28a745; }}
                #leave-status {{ border-left-color: #17a2b8; }}
                .log-box {{ background: #212529; color: #f8f9fa; font-family: monospace; padding: 15px; border-radius: 4px; max-height: 150px; overflow-y: auto; white-space: pre-wrap; font-size: 13px; margin-top: 10px; }}
                .flex-inputs {{ display: flex; gap: 15px; align-items: center; margin-top: 10px; }}
                .badge {{ background: #e2e3e5; padding: 3px 8px; border-radius: 4px; font-size: 14px; font-weight: normal; }}
            </style>
        </head>
        <body>
            <h2>🤖 AlphaTech Solutions - Advanced Intern Suite</h2>
            
            <!-- 1. RAG Search Card -->
            <div class="card">
                <h3>1. AI Intern Assistant</h3>
                <p>Query the indexed <b>knowledge.txt</b> context parameters:</p>
                <div style="display: flex; gap: 10px;">
                    <input type="text" id="question" placeholder="e.g., What are the official working hours?">
                    <button onclick="askAI()">Ask AI</button>
                </div>
                <div id="result" style="display:none;"></div>
            </div>

            <!-- 2. HR Stipend & Live Audit Card -->
            <div class="card">
                <h3>2. HR Stipend Reimbursements</h3>
                <p>Available learning stipend balance: <b>₹{STIPEND_BALANCE:,}</b></p>
                <button class="claim-btn" onclick="triggerClaimPipeline()">Execute Stipend Claim (₹15,000)</button>
                <div id="claim-status" style="display:none;"></div>
                
                <h4 style="margin-top: 20px; margin-bottom: 5px;">📜 Live Transaction Log Stream</h4>
                <div style="margin-bottom: 10px;">
                    <button onclick="refreshLogs()" style="padding: 5px 10px; font-size: 12px; background-color: #6c757d;">🔄 Refresh Log Stream</button>
                    <button onclick="downloadCSV()" class="download-btn">📥 Export to CSV</button>
                </div>
                <div id="log-stream" class="log-box">Click refresh to load audit trail history logs...</div>
            </div>

            <!-- 3. Emergency Leave Window Calculator Card -->
            <div class="card">
                <h3>3. Emergency Leave Notice Validator</h3>
                <p>Verify if your emergency leave notification adheres to the strict <b>2-hour advance notice window</b> rule.</p>
                <div class="flex-inputs">
                    <div>
                        <label>Shift Start Time (IST):</label><br>
                        <input type="time" id="shiftStart" value="09:00">
                    </div>
                    <div>
                        <label>Time Reported to Lead:</label><br>
                        <input type="time" id="reportTime">
                    </div>
                    <button class="verify-btn" onclick="verifyLeaveWindow()" style="margin-top: 18px;">Check Eligibility</button>
                </div>
                <div id="leave-status" style="display:none;"></div>
            </div>

            <script>
                async function askAI() {{
                    const q = document.getElementById('question').value;
                    const resDiv = document.getElementById('result');
                    if (!q) return alert("Please enter a question.");
                    resDiv.style.display = 'block'; resDiv.innerText = 'Searching context...';
                    try {{
                        const response = await fetch('/chat', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ question: q }})
                        }});
                        const data = await response.json();
                        resDiv.innerText = data.response || data.error;
                    }} catch (err) {{ resDiv.innerText = 'Error connecting to server.'; }}
                }}

                async function triggerClaimPipeline() {{
                    const statusDiv = document.getElementById('claim-status');
                    statusDiv.style.display = 'block'; statusDiv.innerText = 'Routing claim request...';
                    try {{
                        const response = await fetch('/claim-stipend', {{ method: 'POST' }});
                        const data = await response.json();
                        if (response.ok) {{
                            statusDiv.innerHTML = `✅ <b>Success!</b> ${{data.message}}<br><small>Reference ID: ${{data.transaction_id}}</small>`;
                            refreshLogs();
                        }} else {{ statusDiv.innerText = `❌ Error: ${{data.detail}}`; }}
                    }} catch (err) {{ statusDiv.innerText = 'Error connecting to HR pipeline.'; }}
                }}

                async function refreshLogs() {{
                    const logBox = document.getElementById('log-stream');
                    try {{
                        const response = await fetch('/get-audit-logs');
                        const data = await response.json();
                        logBox.innerText = data.logs || "No logs recorded yet.";
                    }} catch (err) {{ logBox.innerText = "Error reading log history."; }}
                }}

                function downloadCSV() {{
                    window.open('/download-csv', '_blank');
                }}

                async function verifyLeaveWindow() {{
                    const shiftStart = document.getElementById('shiftStart').value;
                    const reportTime = document.getElementById('reportTime').value;
                    const statusDiv = document.getElementById('leave-status');
                    if (!reportTime) return alert("Please select the time you reported the leave.");
                    
                    statusDiv.style.display = 'block';
                    statusDiv.innerText = 'Calculating timeframe parameters...';
                    
                    try {{
                        const response = await fetch('/verify-leave', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ shift_start_time: shiftStart, report_time: reportTime }})
                        }});
                        const data = await response.json();
                        if (data.eligible) {{
                            statusDiv.style.backgroundColor = '#d4edda';
                            statusDiv.style.borderColor = '#28a745';
                            statusDiv.innerHTML = `💚 <b>Valid Notice Window:</b> ${{data.message}}`;
                        }} else {{
                            statusDiv.style.backgroundColor = '#f8d7da';
                            statusDiv.style.borderColor = '#dc3545';
                            statusDiv.innerHTML = `💔 <b>Policy Violation:</b> ${{data.message}}`;
                        }}
                    }} catch (err) {{ statusDiv.innerText = 'Error verification routing.'; }}
                }}
                
                window.onload = refreshLogs;
            </script>
        </body>
    </html>
    """

@app.post("/chat")
def chat_with_ai(request: QueryRequest):
    try:
        from rag_engine import ask_rag
        return {"query": request.question, "response": ask_rag(request.question)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/claim-stipend")
def claim_stipend():
    import uuid
    from rag_engine import log_transaction
    txn_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    amount = 15000
    status = "Approved"
    try:

        log_transaction(txn_id, amount, status)
        return {"transaction_id": txn_id, "amount": amount, "status": status, "message": "Stipend claim processed successfully."}           
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process stipend claim: {str(e)}")     
              
    