from app import create_app
from app.background_tasks import start_session_monitor


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
    
    try:
        app.run(debug=True, use_reloader=False)  # use_reloader=False prevents double execution
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Shutting down...")
        print("="*60)
        from app.background_tasks import stop_session_monitor
        stop_session_monitor()
        print("\n✓ Shutdown complete")
