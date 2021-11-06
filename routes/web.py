from flask import Flask, send_file
import os

def load_web_routes(app: Flask, *args, **kwargs):
    """ 
        Params:
            app - The main flask app instance

        This function loads the API routes when called.
    """

    @app.route('/download/bin/watch-binary')
    def download_binary():
        """
        Returns binary file for the watch to download
        """
        file_name = "watch_binary.exe"
        bin_path = os.getenv('BIN_PATH')
        full_path = os.path.join(os.getcwd(), bin_path, file_name)
        return send_file(full_path, attachment_filename=file_name)