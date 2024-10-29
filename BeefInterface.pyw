import sys
import google.generativeai as genai
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

# ! Colors
bg_color = "#121212"  # Darker Gray
fg_color = "#E0E0E0"  # Light Gray
input_bg_color = "#1F1F1F"  # Slightly lighter gray for the input box
user_color = "#00BFA5"  # Light teal color for user messages
bot_color = "#BB86FC"  # Light purple color for bot messages

# ! Ask for user input for prompt, then wrap prompt in parentheses

user_inputted_prompt = simpledialog.askstring(title="AI Prompt",prompt="Please enter your desired AI prompt. \nThis tells the AI how to act:")
user_inputted_prompt_quoted = f'"{user_inputted_prompt}"'
print("Starting Gemini with prompt: " + user_inputted_prompt_quoted)

# ! Ask for User input google api key

user_inputted_key = simpledialog.askstring(title="AI Key",prompt="Please enter your Google Gemini AI Api Key:")
print("Using key " + user_inputted_key + "!")

# ! Configure the gemini AI

genai.configure(api_key=user_inputted_key)

generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction=user_inputted_prompt_quoted,
)

chat_session = model.start_chat(
    history=[]
)

# ! End gemini configuration
# ! --------------------------
# ! Begin Main GUI 

# create the main window
root = tk.Tk()
root.title("BeefInterface")
root.geometry("500x700")  # set the size of the window

root.config(bg=bg_color)

# Create a style for the scrollbar
style = ttk.Style()
style.configure('TScrollbar', background='black', troughcolor='black', arrowcolor='white')

# create a frame for the chat history (output)
chat_frame = tk.Frame(root, bg=bg_color)
chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, style='TScrollbar')
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# create a scrolled text box for chat history
output_box = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED, bg=bg_color, fg=fg_color, font=("Microsoft New Tai Lue", 12), bd=0, highlightthickness=0)
output_box.pack(fill=tk.BOTH, expand=True)

output_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_box.yview)

# create an input frame
input_frame = tk.Frame(root, bg=bg_color)
input_frame.pack(fill=tk.X, pady=10)

# create an input box for user text entry
input_box = tk.Entry(input_frame, bg=input_bg_color, fg=fg_color, font=("Microsoft New Tai Lue", 14), bd=0, insertbackground=fg_color)
input_box.pack(side=tk.LEFT, fill=tk.X, padx=10, expand=True)

# create a send button
send_button = tk.Button(input_frame, text="Send", command=lambda: handle_input(), bg=bot_color, fg=fg_color, font=("Microsoft New Tai Lue", 12), bd=0)
send_button.pack(side=tk.RIGHT, padx=10)

def on_closing():
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

def handle_input():
    # get user input from the text box
    user_input = input_box.get()
    
    if not user_input.strip():
        return
    
    # clear the text box for the next input
    input_box.delete(0, tk.END)
    
    # process the input and get the response
    response = chat_session.send_message(user_input)
    model_response = response.text
    
    # display the user's message in the output box
    output_box.config(state=tk.NORMAL)
    output_box.insert(tk.END, f'You: {user_input}\n', 'user')
    
    # display the bot's response in the output box
    output_box.insert(tk.END, f'Bot: {model_response}\n\n', 'bot')
    output_box.config(state=tk.DISABLED)
    
    # update the session history
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})
    
    # scroll to the end of the text box
    output_box.see(tk.END)

# configure the text tag colors
output_box.tag_config('user', foreground=user_color)
output_box.tag_config('bot', foreground=bot_color)

# bind the Enter key to send the message
input_box.bind("<Return>", lambda event: handle_input())

# ! END

root.mainloop()