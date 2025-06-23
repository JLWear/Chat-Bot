import uuid

class ContextManager:
    def __init__(self):
        self.contexts = {}

    def create_context(self):
        context_id = str(uuid.uuid4())
        self.contexts[context_id] = {
            "stage": "ask_interest",
            "data": {}
        }
        return context_id

    def update_context(self, context_id, stage=None, data=None):
        if context_id in self.contexts:
            if stage:
                self.contexts[context_id]["stage"] = stage
            if data:
                self.contexts[context_id]["data"].update(data)

    def get_context(self, context_id):
        return self.contexts.get(context_id, None)

    def clear_context(self, context_id):
        if context_id in self.contexts:
            del self.contexts[context_id]
