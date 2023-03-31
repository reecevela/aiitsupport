from chatbot import ChatBot

chatbot_instance = ChatBot()

user_input = "How to reset a Windows Password?"
response = chatbot_instance.process_input(user_input)

print("Chatbot response:", response)
