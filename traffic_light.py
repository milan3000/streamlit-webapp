def generate_traffic_light_html(state, period, next_state):
    # Fixed colors for the three circles
    colors = ["red", "yellow", "green"]
    textcolors = ["darkgreen", "#8B8000", "darkred"]
    # Opacities based on the state
    opacities = [1.0 if i == state else 0.1 for i in range(3)]
    
    #determing direction of arrow to next state
    if state == 0:
        arrow = "&nearr;"
    elif state == 1:
        if next_state==0:
            arrow= "&searr;"
        elif next_state==2:
            arrow = "&nearr;"
    elif state== 2:
        arrow = "&searr;"
        
    # HTML code for the traffic light
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            .container {{
                position: relative;
                width: 8vw;
                height: 20vw;
                border-radius: 1.6vw;
                overflow: hidden;
                background-color: #595959;
            }}

            .circle {{
                position: absolute;
                width: 6vw;
                line-height: 6vw;
                height: 6vw;
                border-radius: 50%;
                font-size: 30px;
                text-align: center;
            }}

            .red {{
                background-color: {colors[0]};
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                opacity: {opacities[0]};
            }}

            .yellow {{
                background-color: {colors[1]};
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                opacity: {opacities[1]};
                color : {textcolors[1]}
                
            }}

            .green {{
                background-color: {colors[2]};
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                opacity: {opacities[2]};
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="circle red"><b>{f"{period}h{arrow}" if state==0 else ""}</b></div>
            <div class="circle yellow"><b>{f"{period}h{arrow}" if state==1 else ""}</b></div>
            <div class="circle green"><b>{f"{period}h{arrow}" if state==2 else ""}</b></div>
        </div>
    </body>
    </html>
    """

    return html_code