# (C) Antonio Maulucci 2023 - http://www.antomau.com

from io import open

from flask import Flask, render_template, request
import os
import subprocess
# from flask_autoindex import AutoIndex

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def index():
    # If the request method is GET, render the login template
    return render_template('index.html')

@app.route('/musicar', methods=['GET', 'POST'])
def download():
    # se invece di post si deve usare post
    if request.method == "POST":
        # ottieni operazione
        operation = request.form.get('operation')
        # ottieni url del video
        url = request.form['videourl']
        # ottieni nome del file di output
        outfilename = request.form['outputfile']
        if (outfilename == ""):
            outfilename = "default.mp3"
        # dichiara una variabile per i risultati
        result = ""
        # dichiara una variabile per il comando
        comando = ""
        # in base all'operazione esegui i comandi
        if (operation == "video"):
            comando = "yt-dlp " + " -o ./src/static/" + outfilename + " -f bestvideo,bestaudio " + url
        elif (operation == "music"):
            comando = "yt-dlp " + " -o ./src/static/" + outfilename + " -f bestaudio " + url
        elif (operation == "musicar"):
            comando = "yt-dlp " + " -o ./src/static/" + outfilename + " -f bestaudio " + "-x --audio-format mp3" + " --audio-quality 128k " + url
        elif (operation == "custom"):
            comando = "yt-dlp " + " -o ./src/static/" + outfilename + " -f " + request.form['formato'] + " " + url
        elif (operation == "getFormat"):
            comando = "yt-dlp " + " -F " + url

        result = subprocess.check_output(comando, shell=True)
    else:
        return ("non scaricato")
    return result


@app.route('/path', methods=['GET', 'POST'])
def path():
    comando = "pwd"
    result = subprocess.check_output(comando, shell=True)

    # retval = result + pycwd
    # return retval
    return result


@app.route('/pypath', methods=['GET', 'POST'])
def pypath():
    return os.getcwd()


@app.route('/list', methods=['GET', 'POST'])
def list():
    try:
        # Get the list of all files in the current directory
        # files = [f for f in os.listdir("./src/templates/downloaded") if os.path.isfile(f)]
        directory_path = './src/static'
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        html_content = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n\t<title>Download Page</title>\n</head>\n<body>\n\t<h1>Download Page</h1>\n\t<ul>\n'
        for file in files:
            # download_link = f'\t\t<li><a href="static{file}">{file}</a></li>\n'
            download_link = '<li><a href="{{ url_for(\'static\', filename=\'' +  file + '\')}}">' + file + '</a></li>'
            html_content += download_link
        html_content += '\t</ul>\n</body>\n</html>'
        with open('./src/templates/downloaded/list.html', 'w') as html_file:
            html_file.write(html_content)
        return render_template('./downloaded/list.html')
    except Exception as e:
        print(e)
        return "error"


@app.route('/clean', methods=['GET', 'POST'])
def clean():
    directory_path = './src/static'
    try:
        mp3_files = [f for f in os.listdir(directory_path) if f.endswith('.mp3')]
        for mp3_file in mp3_files:
            file_path = os.path.join(directory_path, mp3_file)
            os.remove(file_path)
        return "deleted"
    except Exception as e:
        print(f"Error: {e}")
        return "not deleted"

# @app.route('/list', methods=['GET', 'POST'])
# def listFiles():
#     ppath = "/downloaded"  # update your own parent directory here
#     AutoIndex(app, browse_root=ppath)



    # app.run(host='0.0.0.0', port=870)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8070, debug=True, threaded=True)
