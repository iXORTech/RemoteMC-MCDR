class IndexTemplate:
    content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to RemoteMC-MCDR!</title>
        <meta charset="utf-8">
        <link href="../static/css/style.css" rel="stylesheet" type="text/css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
        <script src="https://unpkg.com/feather-icons"></script>
    </head>
    <body>
    <div id="page-wrapper">
        <div class="index-container">
            <div class="content">
                <h1>Welcome to RemoteMC-MCDR!</h1>
                <hr>
                <p><b>Version </b>{{ version_info }}</p>
                <hr>
                <br>
                <p>If you see this page, the built-in Flask web server of RemoteMC-MCDR is successfully installed and
                    working.</p>
                <br>
                <footer>
                    <hr>
                    <a href="https://github.com/iXORTech/RemoteMC-MCDR/issues">Report a bug</a>
                    <hr>
                    <a href="https://github.com/iXORTech"><i data-feather="github"></i></a>
                    | Powered by <a href="https://ixor.tech">iXOR Technology</a> with 💗.
                    <br>HTML theme designed by <a href="https://github.com/athul/archie">Archie Theme</a>,
                    modified by <a href="https://github.com/KevinZonda">@KevinZonda</a>.
                </footer>
            </div>
        </div>
    </div>
    <script>feather.replace()</script>
    </body>
    </html>
    """
