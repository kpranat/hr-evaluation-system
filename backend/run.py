from app import create_app
from app.background_tasks import start_session_monitor
import os


app = create_app()

if __name__ == '__main__':
    # Start background session monitoring
    print("\n" + "="*60)
    print("Starting HR Evaluation System Backend")
    print("="*60)
    
    # Start monitoring for stale exam sessions
    # Check every 30 seconds, suspend after 2 minutes of inactivity
    monitor = start_session_monitor(app, check_interval=30, inactivity_threshold=120)
    
    print("\n🚀 System ready!")
    print("="*60 + "\n")
    
    # Get port from environment variable (Render sets this automatically)
    # Default to 5000 for local development
    port = int(os.getenv('PORT', 5000))
    
    try:
        # host='0.0.0.0' allows external connections (required for deployment)
        # debug=False in production (Render sets environment variables)
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Shutting down...")
        print("="*60)
        from app.background_tasks import stop_session_monitor
        stop_session_monitor()
        print("\n✓ Shutdown complete")
