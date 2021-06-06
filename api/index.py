from flask import Flask, render_template, jsonify, request
from pprint import PrettyPrinter, pprint
import json
import requests
from  kintone_dl import data_select,data_download


# app = Flask(__name__)
app = Flask(__name__, static_folder='../static', template_folder='../')
app.config['JSON_AS_ASCII'] = False  # jsonを文字化けせずに返すため


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/kintone_dl', methods=['GET'])
def kintone_dl():
    """
    kintoneからイメージのダウンロード
    """

    listData=data_select()
    data_download(listData)

    return jsonify(listData), 200




@app.route('/api_01')
def api_01():

    print(request.args)

    name = request.args.get('name', '')
    print(name)

    dictTemp = {}
    dictTemp['data'] = 'データは{}です'.format(name)

    return jsonify(dictTemp)


def data_insert(listData, domain, app_id, api_token):
    """
    kintoneへのデータ挿入
    """

    url = "https://{}.cybozu.com/k/v1/records.json".format(domain)

    headers = {"X-Cybozu-API-Token": api_token,
               "Content-Type": "application/json"}

    listRecords = []
    for dictTemp in listData:
        dictData = {}
        for key, val in dictTemp.items():
            dictData[key] = {"value": val}

        listRecords.append(dictData)

    params = {
        "app": app_id,
        "records": listRecords
    }

    # pprint(params)
    resp = requests.post(url, json=params, headers=headers)
    # print(resp.text)


@app.route('/api_02', methods=["POST"])
def api_02():

    request_data = json.loads(request.data)

    # pprint(request_data)

    listData = []
    for row in request_data['rows']:
        # pprint(row)
        for cnt in range(5):
            if row[cnt+2] != "":
                sag = '{:02d}_{}'.format(row[0], row[1])
                dictTemp = {'作業NO': 1,
                            '作業': sag, '測定回': cnt+1, '時間': float(row[cnt+2])}
                listData.append(dictTemp)

    app_id = int(request_data['app_id'])
    domain = request_data['domain']
    api_token = request_data['api_token']

    data_insert(listData, domain, app_id, api_token)

    # print(request_data)

    dctData = {}
    # dctData['初期値'] = 'なし'
    # dctData['データ'] = request_data

    return jsonify({})


@app.route('/api_03', methods=["POST"])
def api_03():

    request_data = json.loads(request.data)

    pprint(request_data)

    request_data['追加データ'] = 'api_03で追加したデータ'

    return jsonify(request_data)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
