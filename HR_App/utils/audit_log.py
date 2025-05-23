import logging

audit_logger = logging.getLogger('audit')

def log_audit_event(user, action, details):
    username = user.username if user and user.is_authenticated else 'Anonymous'
    audit_logger.info(details, extra={'action': action, 'user': username})
