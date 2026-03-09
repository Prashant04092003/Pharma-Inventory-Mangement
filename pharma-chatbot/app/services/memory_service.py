class MemoryService:
    _memory = {}

    @classmethod
    def get_history(cls, session_id: str):
        return cls._memory.get(session_id, [])

    @classmethod
    def save_message(cls, session_id: str, role: str, message: str):
        if session_id not in cls._memory:
            cls._memory[session_id] = []

        cls._memory[session_id].append({
            "role": role,
            "message": message
        })

        # Keep only last 10 messages to avoid long prompts
        cls._memory[session_id] = cls._memory[session_id][-10:]