import extract
import os

from flask import Flask, render_template, request
from flask_uploads import patch_request_class

app = Flask(__name__)
patch_request_class(app)


def write(front_or_rear, extraction):
    if not os.path.exists('./extraction'):
        os.mkdir('./extraction')
    with open('./extraction/%s.csv' % front_or_rear, 'a') as out_file:
        for i in extraction:
            out_file.write(' '.join(str(j) for j in i))
            out_file.write('\n')
        out_file.close()


@app.route('/front', methods=['GET', 'POST'])
def front():
    if request.method == 'POST':
        extraction = extract.extract(request.files['file'], 'front')
        write('front', extraction['data'])
        return extraction

    return render_template('front.html')


@app.route('/rear', methods=['GET', 'POST'])
def rear():
    if request.method == 'POST':
        extraction = extract.extract(request.files['file'], 'rear')
        write('rear', extraction['data'])
        return extraction

    return render_template('rear.html')


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
