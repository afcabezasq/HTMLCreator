import pandas as pd
import os
from datetime import datetime, timedelta

def main():
    df = pd.read_csv("./data/chat_conversation_multi_day.csv") # Modify accorginly
    
    date_format = "%Y/%m/%d %H:%M:%S" #Change acorginly
    
    df = df.rename(columns={  #I modified column name to be consistent with my mock data modify acorginly
    "Sender": "from",
    "Receiver": "to",
    "Timestamp": "date",
    "Text": "message",
    "ChatGroup": "conversation_group"
    })
    df['date'] = pd.to_datetime(df['date'], format=date_format)
    output_folder = "message_html"
    os.makedirs(output_folder, exist_ok=True)
    sender_receiver = {}
    # print(file)
    
    start_date = df['date'].min().replace(hour=0, minute=0, second=0)
    end_date = df['date'].max().replace(hour=23, minute=59, second=59)

    current_date = start_date

    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)

        # Get unique conversation groups
        conversation_groups = df["conversation_group"].dropna().unique()

        for group in conversation_groups:
            # Filter messages for this conversation group and date
            daily_messages = df[
                (df["date"] >= current_date) & 
                (df["date"] < next_date) & 
                (df["conversation_group"] == group)
            ]

            if not daily_messages.empty:
                # Generate HTML content with a chat-style layout
                html_content = f"""
                <html>
                <head>
                    <title>{group} - Messages from {current_date.strftime('%Y-%m-%d')}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
                        .chat-container {{ max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                        .message {{ display: flex; flex-direction: column; margin-bottom: 15px; }}
                        .message-header {{ font-size: 12px; color: #666; margin-bottom: 5px; }}
                        .message-bubble {{ max-width: 70%; padding: 10px; border-radius: 15px; word-wrap: break-word; }}
                        .sender {{ align-items: flex-end; }}
                        .receiver {{ align-items: flex-start; }}
                        .sender .message-bubble {{ background: #AEDFF7; }}  /* Light Blue */
                        .receiver .message-bubble {{ background: #FDCB9E; }} /* Light Orange */
                        .timestamp {{ font-size: 12px; color: #888; text-align: right; margin-top: 5px; }}
                    </style>
                </head>
                <body>
                    <div class="chat-container">
                        <h2 style="text-align:center;">{group} - Messages from {current_date.strftime('%Y-%m-%d')}</h2>
                """

                for _, row in daily_messages.iterrows():
                    if "sender" not in sender_receiver:
                        sender_receiver['sender'] = row['from']
                        sender_receiver['receiver'] = row['to']
                    is_sender = True  # This can be modified dynamically if needed
                    alignment = "sender" if sender_receiver['sender']==row['from'] else "receiver"
                    # print(row)

                    # Add message bubble with sender and time above
                    html_content += f"""
                    <div class="message {alignment}">
                        <div class="message-header">{row['from']} - {row['date'].strftime('%H:%M:%S')}</div>
                        <div class="message-bubble receiver">
                            <p>{row['message']}</p>
                        </div>
                    </div>
                    """

                html_content += "</div></body></html>"

                # Format filename: GroupName_YYYY-MM-DD.html
                safe_group_name = "".join(c for c in group if c.isalnum() or c in (" ", "_")).rstrip()
                file_name = f"{output_folder}/{safe_group_name}_{current_date.strftime('%Y-%m-%d')}.html"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                print(f"Saved: {file_name}")

        # Move to the next day
        current_date = next_date

        print("HTML generation complete!")

if __name__ == "__main__":
    main()