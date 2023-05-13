class StatusTemplate:
    content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Status - RemoteMC-MCDR</title>
        <meta charset="utf-8">
        <style>
            {{ css }}
        </style>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
        <script src="https://unpkg.com/feather-icons"></script>
    </head>
    <body>
    <div id="page-wrapper">
        <div class="index-container">
            <div class="content">
                <h2>Status - RemoteMC-MCDR</h2>
                {{ navbar }}
                <br>
                <h2><b class="h1a">Connections:</b></h2>
                <h3>RemoteMC-Core</h3>
                <p>
                    {% if connection == "Connected" %}
                        <i style="color: {{ compatibility_color }};">[{{ compatibility }}] </i>
                    {% endif %}
                    {{ host }} : {{ port }} - <b>{{ connection }}</b>
                </p>
                <br>
                {{ footer }}
            </div>
        </div>
    </div>
    </body>
    </html>
    """
