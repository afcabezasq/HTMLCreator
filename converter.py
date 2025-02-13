import csv
import os
from datetime import datetime, timedelta

def create_folder(foldername):
    os.makedirs(foldername, exist_ok=True)

def read_csv(filename, date_format="%Y-%m-%d %H:%M:%S"):
    with open(filename,"r",encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        groups = {}
        counter = 0
        for row in reader:
    
            if counter == 0:
                counter =+ 1
                continue 
            if row[3] not in groups:
                groups[row[3]] = {
                    'min_date': datetime.strptime(str(row[0]),date_format),
                    'max_date': datetime.strptime(str(row[0]),date_format),
                    'entries':[row]
                    }
            else:
                groups[row[3]]['entries'].append(row)
                current =  datetime.strptime(str(row[0]),date_format)
                if current < groups[row[3]]['min_date']:
                    groups[row[3]]['min_date'] = current
                if current > groups[row[3]]['max_date']:
                    groups[row[3]]['max_date'] = current
                    
    return groups

def generate_html(groups, date_format="%Y-%m-%d %H:%M:%S", output_folder="message_html"):
    create_folder(output_folder)
    for g in groups:
        groups[g]['entries'] = sorted(groups[g]['entries'], key=lambda x: datetime.strptime(x[0],date_format))
        
        start = datetime.strptime(groups[g]['entries'][0][0],date_format)
        start = start - timedelta(hours=start.hour) - timedelta(minutes=start.minute) - timedelta(seconds=start.second)
        
        end = datetime.strptime(groups[g]['entries'][-1][0],date_format)
        end = end - timedelta(hours=end.hour) - timedelta(minutes=end.minute) - timedelta(seconds=end.second)
        end_date = end + timedelta(days=1)
        index = 0
        current_date = start
        while index<len(groups[g]['entries']) and current_date < end_date:
            next_date = current_date + timedelta(days=1)
            entries_by_day = []
            while (index<len(groups[g]['entries']) and datetime.strptime(groups[g]['entries'][index][0],date_format) >= current_date 
                   and datetime.strptime(groups[g]['entries'][index][0], date_format) < next_date
                   ):
                entries_by_day.append(groups[g]['entries'][index])
                index += 1
            if len(entries_by_day) == 0:
                current_date = next_date
                continue
            html_content = f"""
                <html>
                <head>
                    <title>{g}_{current_date.strftime('%Y-%m-%d')}</title>
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
                        .tags {{ display: flex;  }}
                    </style>
                </head>
                <body>
                    <div class="chat-container">
                        <h2 style="text-align:center;">{g} - Messages from {current_date.strftime('%Y-%m-%d')}</h2>
                """
            sender_receiver = {}
            messaage_id = 0
            for date, sender, receiver, chatgroup, text in entries_by_day:
                print(text)
                if "sender" not in sender_receiver:
                    sender_receiver['sender'] = sender
                    sender_receiver['receiver'] = receiver
                alignment = "sender" if sender_receiver['sender'] == sender else "receiver"
                html_content += f"""
                    <div class="message {alignment}">
                        <div class="message-header">{sender} - {date}</div>
                        <div class="message-bubble receiver">
                            <p>{text}</p>
                        </div>
                        <div class="tags" >
                            <p info="true" style="visibility: hidden;">
                                {date};;{sender};;{receiver};;{chatgroup};;{text}
                            </p>
                            <input type="checkbox" id="remove-{messaage_id}" name="remove-tag" value="Remove" onchange="change(this.id)"  haschecked="false">
                            <label for="remove-tag"> Remove </label><br>
                        </div>
                    </div>
                    """
                messaage_id += 1
            html_content += f"<div people=\"{sender_receiver['sender'] };;{sender_receiver['receiver'] }\"></div>\n"
            html_content += """</div>
            </body>
            <script>
                const tags = document.querySelectorAll('input')
                    tags.forEach(t => {
                        if(t.getAttribute('haschecked') == "true"){
                            t.checked = true;
                        }else{
                            t.checked = false;
                        }
                    })

                function change(id){
                    console.log(id)
                    tag = document.querySelector("#"+id)
                    
                    if(tag.getAttribute('haschecked') == "true"){
                        tag.checked = false;
                        tag.setAttribute('haschecked',"false")
                    }else{
                        tag.checked = true;
                        tag.setAttribute('haschecked',"true")
                    }
                }
            </script>
            </html>"""
            safe_group_name = g.replace(" ","")
            file_name = f"{output_folder}/{safe_group_name}_{current_date.strftime('%Y-%m-%d')}.html"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(html_content)    
            print(f"Saved: {file_name}")
                     
            current_date = next_date
        

        
def main():
    
    g = read_csv("data/chat_conversation_multi_day.csv")
    generate_html(g)


if __name__ == "__main__":
    main()