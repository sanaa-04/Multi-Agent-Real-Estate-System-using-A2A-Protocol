
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from shared.models import A2AResponse

resp = A2AResponse(task_id="1", status="success")
try:
    print(resp.status_code)
except AttributeError as e:
    print(f"CAUGHT: {e}")
