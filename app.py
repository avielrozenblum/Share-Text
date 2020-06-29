from flask import Flask
import eel
import threading

flsk = Flask("Aviel API Server", static_url_path='')
flsk.secret_key = "vnergiv3289ynvow002n3invwoifjivjneoibn9j48ibhebfvbdfBYVDS43"

eel.init('web')

# this is the data that sent in eel program
data = {"type": "", "content": "", "file_name": "", "file_type": ""}

# receive data from javascript in eel
@eel.expose
def send_data(rcvd):
    global data
    data = rcvd


# flask function that send data to client side with api
@flsk.route('/data', methods=["GET"])
def get_data():
    global data
    content = repr(data["content"])
    content = content[1:content.rfind("'")]
    # check if file or text. if it's file ==>
    if not data["file_name"] == "":
        # send the file to client side
        f = "<script>\nvar blob = new Blob([\'" + content + "\'], { type: '" + data['file_type'] + ";charset=utf-8' });\nvar file = new File([blob], '"+data['file_name']+ "', {type: '"+ data['file_type'] +"'});\nconst url = window.URL.createObjectURL(blob);\nconst a = document.createElement('a');\na.style.display = 'none';\na.href = url;\na.download = '" + data['file_name'] + "';\na.click();\nwindow.URL.revokeObjectURL(url);\n</script>"
        return f
    else:
        return data["content"]


def start_eel():
    eel.start('main.html', size=(800, 500), port=0)  # python will select free ephemeral ports.


threading.Thread(target=start_eel, ).start()
flsk.run(host='0.0.0.0', port='25391')


