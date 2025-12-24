def convert_time(duration_in_seconds):
    days = int(duration_in_seconds // 86400)
    hours = int((duration_in_seconds % 86400) // 3600)
    minutes = int((duration_in_seconds % 3600) // 60)
    secs = int(duration_in_seconds % 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:  # Always show seconds if nothing else
        parts.append(f"{secs}s")
    
    return " ".join(parts)