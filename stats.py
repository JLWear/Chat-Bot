import time
from collections import defaultdict

class ChatbotStats:
    def __init__(self):
        self.total_conversations = 0
        self.total_messages = 0
        self.conversation_durations = []
        self.intent_counts = defaultdict(int)
        self.current_conversations = {}

    def start_conversation(self, conversation_id):
        self.total_conversations += 1
        self.current_conversations[conversation_id] = {
            "start_time": time.time(),
            "message_count": 0
        }

    def end_conversation(self, conversation_id):
        if conversation_id in self.current_conversations:
            duration = time.time() - self.current_conversations[conversation_id]["start_time"]
            self.conversation_durations.append(duration)
            del self.current_conversations[conversation_id]

    def log_message(self, conversation_id, intent="unknown"):
        self.total_messages += 1
        self.intent_counts[intent] += 1
        if conversation_id in self.current_conversations:
            self.current_conversations[conversation_id]["message_count"] += 1

    def get_average_conversation_duration(self):
        if self.conversation_durations:
            return sum(self.conversation_durations) / len(self.conversation_durations)
        return 0

    def get_most_common_intent(self):
        if self.intent_counts:
            return max(self.intent_counts, key=self.intent_counts.get)
        return None

    def print_stats(self):
        print(f"Total conversations: {self.total_conversations}")
        print(f"Total messages: {self.total_messages}")
        print(f"Average conversation duration: {self.get_average_conversation_duration():.2f} seconds")
        print(f"Most common intent: {self.get_most_common_intent()}")
