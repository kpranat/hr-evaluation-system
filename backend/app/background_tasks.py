"""
Background Tasks for Exam Session Monitoring
Monitors active exam sessions for connection loss and automatically suspends stale sessions.
"""

import threading
import time
from datetime import datetime, timedelta
from app.extensions import db
from app.models import ProctorSession, IntegrityLog


class SessionMonitor:
    """Monitor for detecting and suspending stale exam sessions"""
    
    def __init__(self, app, check_interval=30, inactivity_threshold=120):
        """
        Initialize session monitor
        
        Args:
            app: Flask application instance
            check_interval: Seconds between checks (default: 30)
            inactivity_threshold: Seconds of inactivity before suspension (default: 120)
        """
        self.app = app
        self.check_interval = check_interval
        self.inactivity_threshold = inactivity_threshold
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the background monitoring thread"""
        if self.running:
            print("⚠ Session monitor is already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print(f"✓ Session monitor started (checking every {self.check_interval}s, threshold: {self.inactivity_threshold}s)")
    
    def stop(self):
        """Stop the background monitoring thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("✓ Session monitor stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                self._check_stale_sessions()
            except Exception as e:
                print(f"❌ Error in session monitor: {e}")
                import traceback
                traceback.print_exc()
            
            # Wait for next check
            time.sleep(self.check_interval)
    
    def _check_stale_sessions(self):
        """Check for and suspend stale sessions"""
        with self.app.app_context():
            try:
                # Calculate threshold time
                threshold_time = datetime.utcnow() - timedelta(seconds=self.inactivity_threshold)
                
                # Find active sessions that are:
                # 1. Status is 'active'
                # 2. Not already suspended
                # 3. Last activity older than threshold
                stale_sessions = ProctorSession.query.filter(
                    ProctorSession.status == 'active',
                    ProctorSession.is_suspended == False,
                    ProctorSession.last_activity < threshold_time
                ).all()
                
                if stale_sessions:
                    print(f"\n📊 Found {len(stale_sessions)} stale session(s) to suspend")
                
                for session in stale_sessions:
                    try:
                        # Calculate how long it's been inactive
                        inactive_seconds = (datetime.utcnow() - session.last_activity).total_seconds()
                        
                        # Suspend the session
                        session.is_suspended = True
                        session.suspension_reason = 'Connection lost - abnormal termination detected'
                        
                        # Log integrity event
                        integrity_log = IntegrityLog(
                            session_id=session.id,
                            event='CONNECTION_LOST',
                            severity='CRITICAL',
                            details=f'No heartbeat received for {int(inactive_seconds)}s. Last activity: {session.last_activity.strftime("%Y-%m-%d %H:%M:%S")}',
                            timestamp=datetime.utcnow()
                        )
                        db.session.add(integrity_log)
                        
                        print(f"⚠ Suspended session {session.id} (candidate {session.candidate_id}) - inactive for {int(inactive_seconds)}s")
                        
                    except Exception as e:
                        print(f"❌ Error suspending session {session.id}: {e}")
                        db.session.rollback()
                        continue
                
                # Commit all changes
                if stale_sessions:
                    db.session.commit()
                    print(f"✓ Successfully suspended {len(stale_sessions)} stale session(s)")
                    
            except Exception as e:
                print(f"❌ Error checking stale sessions: {e}")
                db.session.rollback()
                import traceback
                traceback.print_exc()


# Global monitor instance
_monitor = None


def start_session_monitor(app, check_interval=30, inactivity_threshold=120):
    """
    Start the session monitoring background task
    
    Args:
        app: Flask application instance
        check_interval: Seconds between checks (default: 30)
        inactivity_threshold: Seconds of inactivity before suspension (default: 120)
    
    Returns:
        SessionMonitor: The monitor instance
    """
    global _monitor
    
    if _monitor is None:
        _monitor = SessionMonitor(app, check_interval, inactivity_threshold)
        _monitor.start()
    
    return _monitor


def stop_session_monitor():
    """Stop the session monitoring background task"""
    global _monitor
    
    if _monitor:
        _monitor.stop()
        _monitor = None


def get_monitor():
    """Get the current monitor instance"""
    return _monitor
