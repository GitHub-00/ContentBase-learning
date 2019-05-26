from __future__ import division
import os
import operator

def get_avg_score(input_file):
    '''
    Args:
        input_file: user ratings
    Return:
        a dict: key: itemid, value: avg_score
    '''

    if not os.path.exists(input_file):
        return {}

    f = open(input_file)
    linenum = 0
    record = {}
    avg_score = {}
    for line in f:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item)<4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if itemid not in record:
            record[itemid] = [0,0]
        record[itemid][0] += rating
        record[itemid][1] += 1

    f.close()
    for itemid in record:
        avg_score[itemid] = round(record[itemid][0]/record[itemid][1],3)
    return avg_score

def get_item_cate(avg_score, input_file):
    '''
    Args:
        avg_score: a dict, key itemid, value average rating score
        input_file: item info file
    Retrun:
        a dict: key itemid value a dict key:cate value: ratio
        a dict: key cate value [itemid, itemid2, itemid3,..]
    '''

    if not os.path.exists(input_file):
        return {},{}
    linenum = 0

    topk = 100
    item_cate = {}
    record = {}
    cate_item_sort = {}
    f = open(input_file)

    for line in f:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item)<3:
            continue
        itemid = item[0]
        cate_str = item[-1]
        cate_list = cate_str.strip().split('|')
        ratio = round(1/len(cate_list),3)
        if itemid not in item_cate:
            item_cate[itemid] = {}

        for fix_cate in cate_list:
            item_cate[itemid][fix_cate] = ratio
    f.close()

    for itemid in item_cate:
        for cate in item_cate[itemid]:
            if cate not in record:
                record[cate] = {}

            itemid_rating_score = avg_score.get(itemid,0)
            record[cate][itemid] = itemid_rating_score
    for cate in record:
        if cate not in cate_item_sort:
            cate_item_sort[cate] = []

        for zuhe in sorted(record[cate].items(),key=operator.itemgetter(1),reverse=True)[:topk]:
            cate_item_sort[cate].append(zuhe[0])

    return item_cate,cate_item_sort

def get_timestamp(input_file):
    if not os.path.exists(input_file):
        return
    linenum = 0
    latest = 0
    f = open(input_file)
    for line in f:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        timestamp = int(item[3])
        if timestamp > latest:
            latest = timestamp
    f.close()
    print(latest)
    #1537799250


if __name__ == '__main__':
    avg_score = get_avg_score('../data/ratings.csv')
    print(len(avg_score))
    print(avg_score['31'])
    item_cate, cate_item_sort = get_item_cate(avg_score, '../data/movies.csv')
    print(item_cate['1'])
    print(cate_item_sort['Children'])
    get_timestamp('../data/ratings.csv')








