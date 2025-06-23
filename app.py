from chatbot import OrientationChatbot

if __name__ == "__main__":
    bot = OrientationChatbot()
    context_id = bot.create_context()

    print("Bot : Bonjour ! Quels sont tes centres d’intérêt ?")

    while True:
        user_input = input("Élève : ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot : Merci pour ta visite, bonne chance dans ton orientation !")
            break

        response = bot.process_message(context_id, user_input)
        print(f"Bot : {response}")
