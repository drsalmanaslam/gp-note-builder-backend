import sys
print("STARTUP: Beginning...", flush=True)

try:
    from main import app
    print("STARTUP: App imported successfully", flush=True)
except Exception as e:
    print(f"STARTUP ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

import uvicorn
import os
port = int(os.environ.get("PORT", 8000))
print(f"STARTUP: Starting uvicorn on port {port}", flush=True)
uvicorn.run(app, host="0.0.0.0", port=port)