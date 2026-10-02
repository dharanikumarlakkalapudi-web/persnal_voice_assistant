from database.sqlite_database import db

class SecurityManager:
    """Manages tool permissions, risk levels, and confirmations."""
    
    RISK_SAFE = 0
    RISK_LOW = 1
    RISK_SENSITIVE = 2
    RISK_DANGEROUS = 3
    RISK_CRITICAL = 4

    def __init__(self):
        pass

    def evaluate_action(self, agent_id, tool_id, risk_level):
        """
        Evaluates if an action is permitted based on the agent's profile and risk level.
        Returns a decision string: "allowed", "confirmation_required", "face_id_required", "denied"
        """
        from configuration.manager import config_manager
        sec_level = config_manager.get('security.level', 'balanced')
        
        # Determine the Face ID threshold based on security level
        face_id_threshold = self.RISK_DANGEROUS
        if sec_level == 'strict':
            face_id_threshold = self.RISK_SENSITIVE
        elif sec_level == 'relaxed':
            face_id_threshold = self.RISK_CRITICAL
            
        if risk_level >= face_id_threshold:
            return "face_id_required"
            
        if risk_level == self.RISK_SAFE or risk_level == self.RISK_LOW:
            return "allowed"
        elif risk_level == self.RISK_SENSITIVE:
            return "confirmation_required"
        
        return "allowed"

    def log_security_event(self, agent_id, tool_id, action, risk_level, decision, result):
        """Logs a security event to the audit log."""
        db.execute(
            "INSERT INTO activity_logs (agent_id, tool_id, action, risk_level, permission_decision, result) VALUES (?, ?, ?, ?, ?, ?)",
            (agent_id, tool_id, action, risk_level, decision, result)
        )
