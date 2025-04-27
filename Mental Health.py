import random
import re
import time
from datetime import datetime

class MentalHealthBot:
    def __init__(self):
        self.name = "SupportBot"
        self.user_name = None
        self.conversation_history = []
        self.crisis_detected = False
        self.session_start_time = datetime.now()
        
        # Keywords for different mental health concerns
        self.concern_keywords = {
            "anxiety": ["anxious", "nervous", "worry", "panic", "stress", "stressed", "overwhelming"],
            "depression": ["depressed", "sad", "hopeless", "unmotivated", "tired", "exhausted", "worthless"],
            "anger": ["angry", "mad", "frustrated", "irritated", "furious", "rage"],
            "loneliness": ["lonely", "alone", "isolated", "no friends", "no one understands"],
            "grief": ["grief", "loss", "died", "death", "passed away", "mourning"],
            "self_harm": ["hurt myself", "self harm", "cutting", "suicidal", "kill myself", "end it all", "die", "suicide"],
            "trauma": ["trauma", "ptsd", "flashback", "nightmare", "abuse", "assault"]
        }
        
        # Resources for different concerns
        self.resources = {
            "general": [
                "Remember to practice self-care: eat well, exercise, and get enough sleep.",
                "Deep breathing exercises can help manage stress in the moment.",
                "Journaling can be a helpful way to process your thoughts and feelings.",
                "Consider reaching out to a mental health professional for additional support."
            ],
            "anxiety": [
                "Try the 5-4-3-2-1 grounding technique: acknowledge 5 things you see, 4 things you can touch, 3 things you hear, 2 things you smell, and 1 thing you taste.",
                "Progressive muscle relaxation can help reduce physical tension from anxiety.",
                "Limiting caffeine and alcohol can help reduce anxiety symptoms."
            ],
            "depression": [
                "Even small accomplishments matter. Try breaking tasks into smaller steps.",
                "Exposure to sunlight and nature can help improve mood.",
                "Regular exercise, even just a short walk, can help release endorphins."
            ],
            "anger": [
                "Taking a brief time-out can help you respond more calmly.",
                "Physical activity can be a healthy outlet for frustration.",
                "Try to identify what's beneath your anger - often there are other emotions underneath."
            ],
            "loneliness": [
                "Consider joining community groups or classes to meet new people.",
                "Volunteering can be a fulfilling way to connect with others.",
                "Digital connections count too - reach out to friends or family, even virtually."
            ],
            "grief": [
                "Grief has no timeline. Be patient with yourself.",
                "Maintaining routines can provide stability during difficult times.",
                "Consider joining a grief support group to connect with others who understand."
            ],
            "trauma": [
                "Grounding techniques can help when you're experiencing flashbacks.",
                "Trauma-informed therapy approaches like EMDR can be helpful.",
                "Establish safety routines that help you feel secure in your environment."
            ]
        }
        
        # Crisis resources
        self.crisis_resources = [
            "If you're in immediate danger, please call emergency services (911 in the US).",
            "National Suicide Prevention Lifeline: 988 or 1-800-273-8255 (US)",
            "Crisis Text Line: Text HOME to 741741 (US)",
            "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/"
        ]
        
        # Supportive responses
        self.supportive_responses = [
            "I hear that you're going through a difficult time.",
            "That sounds really challenging. Thank you for sharing that with me.",
            "I appreciate you opening up about this.",
            "It takes courage to talk about these feelings.",
            "You're not alone in feeling this way.",
            "Your feelings are valid.",
            "It makes sense that you would feel that way given what you're experiencing."
        ]
        
        # Conversation starters and follow-up questions
        self.follow_up_questions = [
            "How long have you been feeling this way?",
            "Have you talked to anyone else about this?",
            "What has helped you cope with similar feelings in the past?",
            "On a scale of 1-10, how intense would you say these feelings are?",
            "Is there anything specific that triggered these feelings?",
            "What would be a small step that might help you feel better right now?",
            "Have you considered speaking with a mental health professional?",
            "What kind of support would be most helpful for you right now?"
        ]
        
        # Greetings
        self.greetings = [
            "Hello! I'm {}, a mental health support chatbot. How are you feeling today?",
            "Hi there! I'm {} and I'm here to provide support. How can I help you today?",
            "Welcome! I'm {}. I'm here to listen and offer support. What's on your mind?"
        ]
        
        # Exit responses
        self.exit_responses = [
            "Take care of yourself. Remember, it's okay to reach out for help when needed.",
            "I hope our conversation has been helpful. Be gentle with yourself.",
            "Thank you for talking with me today. Remember that seeking support is a sign of strength.",
            "Wishing you well. Please don't hesitate to reach out again if you need support."
        ]

    def detect_concerns(self, user_input):
        """Identify potential mental health concerns based on keywords."""
        user_input_lower = user_input.lower()
        detected_concerns = []
        
        # Check for crisis keywords first
        crisis_indicators = self.concern_keywords["self_harm"]
        for word in crisis_indicators:
            if word in user_input_lower:
                self.crisis_detected = True
                detected_concerns.append("crisis")
                break
        
        # Check for other concerns
        for concern, keywords in self.concern_keywords.items():
            if concern != "self_harm":  # Already checked this
                for word in keywords:
                    if word in user_input_lower:
                        detected_concerns.append(concern)
                        break
        
        return detected_concerns if detected_concerns else ["general"]

    def generate_resource_response(self, concerns):
        """Generate a response with relevant resources based on detected concerns."""
        response = ""
        
        # If crisis is detected, prioritize those resources
        if "crisis" in concerns:
            response += "I'm concerned about what you've shared. Your safety is important.\n\n"
            response += random.choice(self.crisis_resources) + "\n\n"
            response += "Would it be possible for you to reach out to one of these resources now?\n\n"
        
        # Add a supportive statement
        response += random.choice(self.supportive_responses) + "\n\n"
        
        # Add resources for each detected concern (up to 2 concerns)
        resource_count = 0
        for concern in concerns:
            if concern != "crisis" and resource_count < 2:
                if concern in self.resources:
                    response += random.choice(self.resources[concern]) + "\n\n"
                    resource_count += 1
        
        # Always include a general resource
        if "general" not in concerns and resource_count < 2:
            response += random.choice(self.resources["general"]) + "\n\n"
        
        # Add a follow-up question
        response += random.choice(self.follow_up_questions)
        
        return response

    def get_greeting(self):
        """Return a random greeting message."""
        return random.choice(self.greetings).format(self.name)

    def get_exit_response(self):
        """Return a random exit message."""
        return random.choice(self.exit_responses)

    def respond(self, user_input):
        """Generate a response based on user input."""
        # Save the user's message to conversation history
        self.conversation_history.append(("user", user_input))
        
        # Check for exit intent
        exit_patterns = ["bye", "goodbye", "exit", "quit", "end", "stop"]
        if any(pattern in user_input.lower() for pattern in exit_patterns):
            exit_response = self.get_exit_response()
            self.conversation_history.append(("bot", exit_response))
            return exit_response
        
        # Check for name if not already known
        if not self.user_name:
            name_match = re.search(r"my name is (\w+)", user_input.lower())
            if name_match:
                self.user_name = name_match.group(1).capitalize()
                response = f"Nice to meet you, {self.user_name}. How are you feeling today?"
                self.conversation_history.append(("bot", response))
                return response
        
        # Detect concerns and generate response
        concerns = self.detect_concerns(user_input)
        response = self.generate_resource_response(concerns)
        
        # Add personalization if we know the user's name
        if self.user_name and random.random() < 0.3:  # 30% chance to use name
            response = f"{self.user_name}, {response}"
        
        # Save the bot's response to conversation history
        self.conversation_history.append(("bot", response))
        return response

    def start_conversation(self):
        """Start an interactive conversation with the user."""
        print(self.get_greeting())
        
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "goodbye", "exit", "quit"]:
                print(f"{self.name}: {self.get_exit_response()}")
                break
                
            # Simulate thinking with a short delay
            print(f"{self.name} is typing...")
            time.sleep(1)  # Adjust the delay as needed
            
            bot_response = self.respond(user_input)
            print(f"{self.name}: {bot_response}")
            
            # If crisis was detected, encourage immediate support
            if self.crisis_detected:
                print(f"{self.name}: I strongly encourage you to reach out to one of the crisis resources I mentioned.")
                print(f"{self.name}: Would you like me to provide those resources again?")

    def export_conversation(self, filename=None):
        """Export the conversation history to a text file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"support_conversation_{timestamp}.txt"
        
        with open(filename, "w") as file:
            file.write(f"Conversation with {self.name} - {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for speaker, message in self.conversation_history:
                if speaker == "user":
                    file.write(f"You: {message}\n\n")
                else:
                    file.write(f"{self.name}: {message}\n\n")
        
        return filename


# If running as a standalone script
if __name__ == "__main__":
    bot = MentalHealthBot()
    bot.start_conversation()