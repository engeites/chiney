import jieba


def tokenize(text):
    seg_list = jieba.cut(text, cut_all=False)
    return seg_list  # 全模式


if __name__ == '__main__':
    pass
