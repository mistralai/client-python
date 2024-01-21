import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from ttkthemes import ThemedStyle

class MistralInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Mistral Interface')

        # Apply the 'arc' theme
        style = ThemedStyle(self)
        style.set_theme("arc")

        # Configure the background
        self.configure(bg='#121212')
        style.configure('TFrame', background='#2E1437')
        style.configure('TLabel', background='#2E1437', foreground='#ffffff')
        style.configure('TButton', background='#ffffff', foreground='#000000')
        style.configure('TCombobox', fieldbackground='#ffffff', foreground='#000000')
        style.configure('TEntry', fieldbackground='#ffffff', foreground='#000000')

        # Variables to store user inputs
        self.api_key_var = tk.StringVar()
        self.api_key_var.set('')  # Initialize with an empty string
        self.model_var = tk.StringVar()
        self.model_var.set('mistral-tiny')
        self.role_var = tk.StringVar()
        self.role_var.set('user')
        self.content_var = tk.StringVar()
        self.content_var.set('Who is the most renowned French painter?')
        self.result_var = tk.StringVar()

        # Create widgets
        self.frame = ttk.Frame(self)
        self.frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.label_api_key = ttk.Label(self.frame, text='Mistral API Key:')
        self.entry_api_key = ttk.Entry(self.frame, textvariable=self.api_key_var, show='*')
        self.label_model = ttk.Label(self.frame, text='Model:')
        self.combo_model = ttk.Combobox(self.frame, textvariable=self.model_var, values=['mistral-tiny', 'mistral-small', 'mistral-medium'])
        self.label_role = ttk.Label(self.frame, text='Role:')
        self.combo_role = ttk.Combobox(self.frame, textvariable=self.role_var, values=['user', 'assistant'])
        self.label_content = ttk.Label(self.frame, text='Content:')

        # New: Use Text instead of Entry for self.entry_content
        self.entry_content = tk.Text(self.frame, wrap="word", height=5, width=100)

        # New: Create a scrollbar for self.entry_content
        self.entry_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.entry_content.yview)
        self.entry_content.config(yscrollcommand=self.entry_scrollbar.set)

        self.button_send_request = ttk.Button(self.frame, text='Send Request', command=self.send_request)
        self.label_result = ttk.Label(self.frame, text='Result:')
        self.result_text = tk.Text(self.frame, height=5, width=50, wrap="word", state=tk.DISABLED)

        # New: Create a scrollbar for self.result_text
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        # Place widgets in the window
        self.label_api_key.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_api_key.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_model.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.combo_model.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_role.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.combo_role.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_content.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_content.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        self.entry_scrollbar.grid(row=3, column=2, pady=5, sticky=tk.NS)
        self.button_send_request.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_result.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.result_text.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        self.scrollbar.grid(row=5, column=2, pady=5, sticky=tk.NS)

        # Configure row and column weights for resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(5, weight=1)

    def send_request(self):
        # Get user inputs
        api_key = self.api_key_var.get()
        model = self.model_var.get()
        role = self.role_var.get()
        content = self.entry_content.get("1.0", tk.END).strip()

        # Create the request body
        request_body = {
            "model": model,
            "messages": [{"role": role, "content": content}]
        }

        try:
            response = self.make_api_request(api_key, request_body)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                self.result_var.set(content)
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, content)
                self.result_text.config(state=tk.DISABLED)
                messagebox.showinfo('Success', 'Request successful!\nContent displayed in the window.')
            else:
                messagebox.showerror('Error', 'Error during the request. Status code: {}'.format(response.status_code))
        except Exception as e:
            messagebox.showerror('Error', 'An error occurred: {}'.format(str(e)))

    def make_api_request(self, api_key, request_body):
        url = 'https://api.mistral.ai/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(api_key)
        }

        # Perform the POST request
        response = requests.post(url, headers=headers, data=json.dumps(request_body))
        return response

if __name__ == "__main__":
    app = MistralInterface()
    app.geometry("800x600")  # Initial window size
    app.mainloop()
