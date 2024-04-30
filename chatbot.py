import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

class ChatApplication:
    def __init__(self, master):
        self.master = master
        master.title("TechGadget Support")

        # Set background color to light blue
        master.configure(bg="lightblue")

        # Download and process icons
        self.user_icon_url = "https://cdn-icons-png.flaticon.com/128/1077/1077114.png"
        self.bot_icon_url = "https://cdn-icons-png.flaticon.com/128/10541/10541409.png"
        self.user_icon = self.process_icon(self.user_icon_url)
        self.bot_icon = self.process_icon(self.bot_icon_url)

        if not self.user_icon or not self.bot_icon:
            print("Failed to download and process icons.")
            return

        # Create a text widget to display the conversation
        self.conversation = tk.Text(master, state='disabled')
        self.conversation.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Create an entry widget for user input
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        # Create a button to send the message
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Create a label to display quit message
        self.quit_message = tk.Label(master, text="You can type 'quit', 'exit' or 'bye' to close the window.", bg="lightblue")
        self.quit_message.grid(row=2, column=0, columnspan=2, pady=(0, 5))

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            self.add_message("Bot", "Goodbye! If you have any more questions, we're here to help.")
            self.master.after(2000, self.master.destroy)  # Wait for 2 seconds before automatically closing
        else:
            self.add_message("You", user_input)
            self.master.after(2000, lambda: self.send_bot_response(user_input))  # Send bot response after 2 seconds
            self.entry.delete(0, tk.END)

    def send_bot_response(self, user_input):
        response = self.get_bot_response(user_input)
        self.add_message("Bot", response)

    def get_bot_response(self, user_input):
        user_input = user_input.lower()
        if user_input in responses:
            return responses[user_input]
        else:
            for key, value in responses.items():
                if user_input in key:
                    return value
            return "I'm sorry, I couldn't understand your query."

    def add_message(self, sender, message):
        self.conversation.configure(state='normal')
        if sender == "You":
            self.conversation.image_create(tk.END, image=self.user_icon)
            self.conversation.insert(tk.END, ": " + message + '\n\n')
        else:
            self.conversation.image_create(tk.END, image=self.bot_icon)
            self.conversation.insert(tk.END, ": " + message + '\n\n')
        self.conversation.configure(state='disabled')
        # Scroll to the bottom of the conversation
        self.conversation.see(tk.END)

    def process_icon(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            icon = Image.open(BytesIO(response.content))
            icon = icon.resize((20, 20))  # Resize icon to desired dimensions
            return ImageTk.PhotoImage(icon)
        else:
            return None

# Define the responses dictionary
responses = {
    "hi": "Hello! Welcome to TechGadget Support. How can I assist you today?",
    "hello": "Hello! Welcome to TechGadget Support. How can I assist you today?",
    "do you have smartwatches": "Yes, we have a variety of smartwatches. You can check them out on our products page.",
    "shipping time": "Shipping usually takes 3-5 business days.",
    "shipping methods": "We offer standard, expedited, and overnight shipping.",
    "return policy": "You can return products within 30 days of receipt for a full refund.",
    "how to return": "To return a product, please visit our returns page for a step-by-step guide.",
    "won’t turn on": "Make sure your gadget is charged. If it still won’t turn on, you can visit our troubleshooting page.",
    "reset device": "To reset your device, hold down the power button for 10 seconds. If that doesn't work, please check the manual for a factory reset.",
    "track order": "You can track your order by visiting our website and logging into your account.",
    "cancel order": "To cancel your order, please contact our customer support team with your order number.",
    "product availability": "Our products are subject to availability. You can check the availability of a specific product on our website.",
    "tech support": "For technical support, please visit our tech support page or contact our support team.",
    "payment methods": "We accept various payment methods including credit/debit cards, PayPal, and bank transfers.",
    "product warranty": "Our products come with a standard one-year warranty. You can also purchase extended warranties for additional coverage.",
    "compatibility": "Please check the product specifications or contact our support team for information regarding compatibility with your device.",
    "product manuals": "You can download product manuals from our website under the support section.",
    "bulk orders": "For bulk orders, please contact our sales team for special pricing and assistance.",
    "promotions": "We offer various promotions and discounts throughout the year. You can sign up for our newsletter to stay updated.",
    "technical specifications": "You can find detailed technical specifications for our products on their respective product pages.",
    "privacy policy": "Our privacy policy outlines how we collect, use, and protect your personal information. You can view it on our website.",
    "security concerns": "We take security seriously. Please contact our security team if you have any concerns regarding the security of our products or website.",
    "unsubscribe": "To unsubscribe from our newsletter, you can click the 'unsubscribe' link at the bottom of any newsletter email.",
    "feedback": "We appreciate your feedback! Please feel free to leave us a review on our website or contact our support team with your suggestions.",
    "bye": "Thank you for visiting TechGadget. If you have more questions, feel free to ask. Goodbye!"
}

# Create the Tkinter application
root = tk.Tk()
app = ChatApplication(root)
root.mainloop()
