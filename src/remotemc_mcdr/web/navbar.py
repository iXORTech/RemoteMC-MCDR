class Navbar:
    @staticmethod
    def get():
        return """
        <hr>
        <a href="/">Home Page</a>
        <b> | </b>
        <a href="/status">Status</a>
        <b> | </b>
        <a href="/about">About</a>
        <hr>
        """