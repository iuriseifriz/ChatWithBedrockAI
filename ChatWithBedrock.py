import customtkinter as ctk
import boto3
import json

# ctk window creation
app = ctk.CTk()
app.geometry("500x600")
app.title("Chat with Bedrock")

ctk.set_appearance_mode("dark")

# credentials
aws_access_key_id = None
aws_secret_access_key = None

# function that create the bedrock reply
def generate_answer(prompt):
    # verify credentials
    if not aws_access_key_id or not aws_secret_access_key:
        return "Please, insert the AWS credentials."

    # connect credentials
    bedrock_runtime = boto3.client(
        'bedrock-runtime',
        region_name='us-east-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    kwargs = {
        "modelId": "amazon.nova-micro-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "inferenceConfig": {
                "max_new_tokens": 1000
            },
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)
    
    try:
        response_body = json.loads(response['body'].read())
        reply_text = response_body.get("output", {}).get("message", {}).get("content", [{}])[0].get("text", "No reply")
    except Exception as e:
        reply_text = f"Error: {e}"

    return reply_text

# function to show the reply
def show_text():
    text = input_text.get("1.0", ctk.END).strip()

    if text:
        reply = generate_answer(text)
        output = f"{reply}"
    else:
        output = "No text was typed."

    # uptade the text box
    reply_box.configure(state="normal")
    reply_box.delete(1.0, ctk.END)
    reply_box.insert(ctk.END, output)
    reply_box.configure(state="disabled")

# config credentials
def config_credentials():
    global aws_access_key_id, aws_secret_access_key

    aws_access_key_id = input_access_key.get()
    aws_secret_access_key = input_secret_key.get()

    if aws_access_key_id and aws_secret_access_key:
        status_label.configure(text="Success!", text_color="green")
    else:
        status_label.configure(text="Please, insert both credentials.", text_color="red")

# interface items
reply_box = ctk.CTkTextbox(app, width=450, height=150, font=("Arial", 12))
reply_box.pack(pady=(15, 10))
reply_box.configure(state="disabled")

label = ctk.CTkLabel(app, text="Type your question:", font=("Arial", 12))
label.pack(pady=5)

input_text = ctk.CTkTextbox(app, height=40, width=450, font=("Arial", 12))
input_text.pack(pady=5)

send_btn = ctk.CTkButton(app, text="Send", command=show_text, font=("Arial", 12), corner_radius=8)
send_btn.pack(pady=(10, 15))

label_access_key = ctk.CTkLabel(app, text="AWS Access Key ID:", font=("Arial", 12))
label_access_key.pack(pady=5)

input_access_key = ctk.CTkEntry(app, width=300, font=("Arial", 12))
input_access_key.pack(pady=5)

label_secret_key = ctk.CTkLabel(app, text="AWS Secret Access Key:", font=("Arial", 12))
label_secret_key.pack(pady=5)

input_secret_key = ctk.CTkEntry(app, width=300, font=("Arial", 12), show="*")
input_secret_key.pack(pady=5)

config_btn = ctk.CTkButton(app, text="Configure Credentials", command=config_credentials, font=("Arial", 12), corner_radius=8)
config_btn.pack(pady=10)

status_label = ctk.CTkLabel(app, text="", font=("Arial", 12))
status_label.pack(pady=5)

label = ctk.CTkLabel(app, text="For Amazon Nova Micro-v1:0 | By Iuri Seifriz", font=("Arial", 12))
label.pack(pady=3)

app.mainloop()
