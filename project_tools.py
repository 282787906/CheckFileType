import requests


def loadFile(url, path):
    imgres = requests.get(url)
    if imgres.status_code == 200:
        with open(path, "wb") as f:
            f.write(imgres.content)

        return imgres.status_code
    else:
        return imgres.status_code

def loadByHeaders(uid):


    imgres = requests.get('http://pre.sstax.cn:81/cs-third/cer/commonForApi/getCommonAccountInfo', params = {'accountSetUid': uid}, headers = {'uid': uid})
    # if imgres.status_code == 200:
    #
    #     return imgres.status_code
    # else:
    #     return imgres.status_code
    return imgres.status_code


imgres = requests.get('http://sstax.cn:1000/cs-third/cer/commonForApi/getCommonAccountInfo',
                      params={'accountSetUid': '20171009-102958-845'}, headers={'uid': '20171009-102958-845'})

if imgres.status_code != 200:
    print(imgres.status_code,imgres.reason)