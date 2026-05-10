import os
import threading
import webbrowser
from app import create_app

app = create_app()

def open_browser():
    port = app.config.get("PORT", 5000)
    webbrowser.open_new(f"http://127.0.0.1:{port}/index")

if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    debug = app.config.get("DEBUG", False)
    
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true" and not debug:
        threading.Timer(1.0, open_browser).start()
        
    app.run(host="127.0.0.1", port=port, debug=debug, use_reloader=debug)
