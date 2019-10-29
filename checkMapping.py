import json

import log
from mysqlHelper import getInfoMapping, getSubjectByTemplateId, updataNewTemplateMapping


def main():
    log.d('查询mapping')
    ret_getFile, data, msg = getInfoMapping()
    if ret_getFile == 0:

        log.d('遍历mapping 根据mapping 中的模板id查询模板明细')
        for row in data:
            mappingId = row.id
            mapping = row.mapping
            template_id = row.template_id
            log.d('  mappingId:', mappingId)
            if mappingId >0:
                ret_getSb, data, msg = getSubjectByTemplateId(template_id)
                if ret_getSb == 0:
                    log.d('  用模板明细中的code对比mapping中的code  替换 mapping的模板明细id')
                    dict = {}
                    for row in data:
                        dict[row.SUBJECT_CODE] = row.id
                    map = json.loads(mapping)
                    if len(dict) < len(map):
                        log.e('模板明细数量小于mapping明细数量')
                        return
                    for item in map:
                        if dict[item['subjectCode']] is not None:
                            item['subjectId'] = dict[item['subjectCode']]
                        else:
                            log.e(dict[item['subjectCode']], "is None", map)
                    mapping = json.dumps(map, ensure_ascii=False)

                    ret_update, msg = updataNewTemplateMapping(mappingId,mapping)
                    if ret_update==0:
                        log.d('保存mappping成功')
                    else:
                        log.w(mappingId,'保存mappping失败:', msg)

                else:
                    log.e('  根据模板id查询模板明细失败：', template_id)


    else:
        log.w('ret:', msg)


if __name__ == "__main__":
    log.i('start main')
    main()
