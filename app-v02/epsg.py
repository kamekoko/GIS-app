list = {'farm_komatsu': 6675}

def getEpsg(data_id):
    val = -1
    for k,v in list.items():
        if k == data_id:
            val = v
    return val
