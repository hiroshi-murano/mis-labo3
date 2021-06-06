import requests
import json
from pprint import pprint
# import base64
# import codecs


domain = 'tox1i0lgjy5s'
app_id = 122
api_token = "MSACsgvPg4vOpDndGe9lR6AZuI7ioCzPS6uLyqg2"


def data_select():
    """
    kintoneのレコードを複数取得
    """

    url = "https://{}.cybozu.com/k/v1/records.json".format(domain)
    headers = {"X-Cybozu-API-Token": api_token,
               "Content-Type": "application/json"}

    params = {
        "app": app_id,
    }

    resp = requests.get(url, json=params, headers=headers)

    print(resp.text)
    dctData = json.loads(resp.text)

    listData = []
    for dictTemp in dctData['records']:
        id = dictTemp['レコード番号']['value']
        title = dictTemp['タイトル']['value']
        answer = dictTemp['回答内容']['value']
        listImage = dictTemp['付箋画像']['value']
        if len(listImage) > 0:
            fileKey = listImage[0]['fileKey']
            listData.append({'id': id, 'title': title, 'fileKey': fileKey,'回答内容':answer})

    return listData


def data_download(listData):
    """
    file download
    """

    url = "https://{}.cybozu.com/k/v1/file.json".format(domain)
    headers = {"X-Cybozu-API-Token": api_token,
               "Content-Type": "application/json"}

    for dictTemp in listData:

        params = {
            "fileKey": dictTemp['fileKey']
        }

        resp = requests.get(url, json=params, headers=headers)
        fname = r'..\static\images\{}.png'.format(dictTemp['id'])
        print(fname)
        f = open(fname, 'bw')
        f.write(resp.content)
        f.close()


if __name__ == "__main__":

    ret = data_select()
    # pprint(ret)
    data_download(ret)
