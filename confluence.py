import numpy as np
import cv2

#可以测试woman、cat、person三个图片，单独去掉注释号即可

# bbox_original = np.loadtxt('woman_bbox.txt')
# path = 'woman.jpg'

# bbox_original = np.loadtxt('cat_bbox.txt')
# path = 'cat.jpg'

bbox_original = np.loadtxt('person_bbox.txt')
path = 'person.jpg'

def imshow(path, bbox):

    img = cv2.imread(path)

    bbox1 = bbox[:, :4].astype(int)

    min_point = [tuple(x) for x in bbox1[:, :2].tolist()]

    max_point = [tuple(x) for x in bbox1[:, 2:4].tolist()]

    for i in range(len(bbox)):
        cv2.rectangle(img, min_point[i], max_point[i], (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def norm(bbox1, bbox2):
    x1min, y1min, x1max, y1max = bbox1[0], bbox1[1], bbox1[2], bbox1[3]
    x2min, y2min, x2max, y2max = bbox2[0], bbox2[1], bbox2[2], bbox2[3]

    lx = max(x1min, x1max, x2min, x2max)-min(x1min, x1max, x2min, x2max)
    ly = max(y1min, y1max, y2min, y2max)-min(y1min, y1max, y2min, y2max)

    xmin = min(x1min, x1max, x2min, x2max)
    ymin = min(y1min, y1max, y2min, y2max)

    x1min = (x1min-xmin)/lx
    y1min = (y1min-ymin)/ly
    x2min = (x2min-xmin)/lx
    y2min = (y2min-ymin)/ly
    x1max = (x1max-xmin)/lx
    y1max = (y1max-ymin)/ly
    x2max = (x2max-xmin)/lx
    y2max = (y2max-ymin)/ly

    p = np.absolute(x1min-x2min)+np.absolute(x1max-x2max) + \
        np.absolute(y1min-y2min)+np.absolute(y1max-y2max)

    return p



def confluence(bbox,threshold):
    
   
    print(30*'-')
    
    bbox_num=[i for i in range(len(bbox))]#对各个bbox进行编号
    
    keep = []

    while len(bbox_num) > 0:
        
        score_min = []#存放每一轮每个bbox最小WP
        loc_set=[]#存放每个bbox的P<阈值的bbox编号
        
        for i in bbox_num:
            score = []#存放bbox[i]的所有WP，然后选出最小
            loc=[]#存放P<threshold的bbox编号
            for j in bbox_num:
                P = norm(bbox[i], bbox[j])
                if P<threshold:
                    loc.append(j)
                    
                if P < 2 and P != 0:
                    WP = P/bbox[i][4]
                    score.append(WP)
                    
                    
            score_min.append(round(min(score), 3))
            loc_set.append(loc)
            
        print('各个bbox最低WP:', score_min)
        print('各bbox的 P<treshold 的另一个bbox编号:',loc_set)
       
        
        index = score_min.index(min(score_min))
        bbox_index=bbox_num[index]
        print('最低score bbox编号:',bbox_index)
        
        keep.append(bbox_index)
        print('最终bbox集合:',keep)
        print('要删除的bbox编号',loc_set[index])
        
        for i in loc_set[index]:
            bbox_num.remove(i)
            
        
        print('剩下bbox:',bbox_num)
        
        
        
        if len(bbox_num)==1:
            keep.append(bbox_num[0])
            print('剩下1个，并入最终bbox',keep)
            break
        
        print(30*'-')
   
    bbox_process = bbox[keep]
    
    return bbox_process


imshow(path, bbox_original)

imshow(path, confluence(bbox_original,0.8))

