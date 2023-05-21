class AboutTemplate:
    content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to RemoteMC-MCDR!</title>
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
                <h1>About - RemoteMC-MCDR</h1>
                {{ navbar }}
                <br>
                <p style="text-align: center;"><b>RemoteMC-MCDR</b></p>
                <p style="text-align: center;">
                    Version {{ version_info }}
                    <br>
                    Built on {{ build_date }}
                    <br>
                    Licensed under: <a href="https://github.com/iXORTech/RemoteMC-Core/blob/main/LICENSE">
                        <b>GNU Affero General Public License v3.0</b>
                    </a>
                    </p>
                <br>
                <h2>Contributors</h2>
                <ul>
                    <li>@Cubik65536 | <a href="https://cubik65536.top"><i data-feather="globe"></i></a> | <a href="https://github.com/Cubik65536"><i data-feather="github"></i></a> | </li>
                </ul>
                <br>
                {{ footer }}
            </div>
        </div>
    </div>
    <script>feather.replace()</script>
    </body>
    </html>
    """
