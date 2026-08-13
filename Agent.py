from fastapi import FastAPI, HTTPException, status, BackgroundTasks
import uuid
from database import get_db_connection

app = FastAPI(title="RBAC Gateway API")

def notify_team_lead(lead_name: str, lead_email: str, user_id: str, resource_id: str, token: str):
    """Simulates an alert sent to the group's Team Lead."""
    print("\n" + "="*50)
    print(f"🚨 ALERT SENT TO TEAM LEAD: {lead_name} ({lead_email})")
    print(f"User '{user_id}' attempted unauthorized access to '{resource_id}'.")
    print(f"Approval Token Generated: {token}")
    print("="*50 + "\n")

@app.get("/")
def home():
    return {"message": "RBAC Gateway API is active"}

@app.get("/api/access")
def check_access(user_id: str, resource_id: str, token: str = None, background_tasks: BackgroundTasks = None):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)

    # 1. Check Group Membership Permission
    rbac_query = """
    SELECT r.resource_name, r.api_endpoint
    FROM user_groups ug
    JOIN group_resources gr ON ug.group_id = gr.group_id
    JOIN resources r ON gr.resource_id = r.resource_id
    WHERE ug.user_id = %s AND r.resource_id = %s
    """
    cursor.execute(rbac_query, (user_id, resource_id))
    permission = cursor.fetchone()

    if permission:
        cursor.close()
        conn.close()
        return {
            "status": "GRANTED",
            "message": f"Access granted for user '{user_id}' via group membership.",
            "data": f"Sensitive payload retrieved from {permission['api_endpoint']}"
        }

    # 2. Check for Approved Token
    if token:
        token_query = """
        SELECT status FROM access_requests 
        WHERE user_id = %s AND resource_id = %s AND approval_token = %s AND status = 'APPROVED'
        """
        cursor.execute(token_query, (user_id, resource_id, token))
        valid_token = cursor.fetchone()
        if valid_token:
            cursor.close()
            conn.close()
            return {
                "status": "GRANTED",
                "message": "Access granted via approved Team Lead token.",
                "data": "Sensitive payload retrieved using approved request token."
            }

    # 3. Handle Unauthorized Access & Alert Team Lead
    lead_query = """
    SELECT u.name AS lead_name, u.email AS lead_email
    FROM group_resources gr
    JOIN groups g ON gr.group_id = g.group_id
    JOIN users u ON g.team_lead_id = u.user_id
    WHERE gr.resource_id = %s
    """
    cursor.execute(lead_query, (resource_id,))
    lead_info = cursor.fetchone()

    approval_token = f"TOKEN_{uuid.uuid4().hex[:8].upper()}"

    if lead_info:
        insert_request = """
        INSERT INTO access_requests (user_id, resource_id, approval_token, status)
        VALUES (%s, %s, %s, 'PENDING')
        """
        cursor.execute(insert_request, (user_id, resource_id, approval_token))
        conn.commit()

        if background_tasks:
            background_tasks.add_task(
                notify_team_lead, 
                lead_info['lead_name'], 
                lead_info['lead_email'], 
                user_id, 
                resource_id, 
                approval_token
            )

    cursor.close()
    conn.close()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "error": "Access Denied",
            "message": f"User {user_id} lacks permission for {resource_id}.",
            "approval_token": approval_token,
            "notified_lead": lead_info['lead_name'] if lead_info else "Unknown"
        }
    )
