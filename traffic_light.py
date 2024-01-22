def generate_traffic_light_html(state):
    # Fixed colors for the three circles
    colors = ["red", "yellow", "green"]

    # Opacities based on the state
    opacities = [1.0 if i == state else 0.1 for i in range(3)]

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
                width: 160px;
                height: 320px;
                border-radius: 20px;
                overflow: hidden;
                background-color: grey;
            }}

            .circle {{
                position: absolute;
                width: 90px;
                height: 90px;
                border-radius: 50%;
            }}

            .red {{
                background-color: {colors[0]};
                top: 10px;
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
            }}

            .green {{
                background-color: {colors[2]};
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                opacity: {opacities[2]};
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="circle red"></div>
            <div class="circle yellow"></div>
            <div class="circle green"></div>
        </div>
    </body>
    </html>
    """

    return html_code