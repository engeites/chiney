import jieba


def doit(text):
    seg_list = jieba.cut_for_search(text)
    return seg_list  # 全模式

if __name__ == '__main__':
    doit("我是你的朋友")