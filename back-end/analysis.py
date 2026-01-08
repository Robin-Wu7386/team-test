# back-end/analysis.py
import sys
from snownlp import SnowNLP

# 解决控制台输出乱码问题
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def analyze(text):
    if not text.strip():
        return 0.5

    # SnowNLP 自动处理中文分词和情感计算
    s = SnowNLP(text)
    score = s.sentiments  # 返回 0到1 之间的浮点数
    return score


if __name__ == "__main__":
    # 获取 Node.js 传过来的参数 (评论内容)
    # sys.argv[0] 是文件名, sys.argv[1] 是第一个参数
    if len(sys.argv) > 1:
        content = sys.argv[1]
        score = analyze(content)
        print(score)  # 把分数打印出来，Node.js 会捕获这个输出
    else:
        print(0.5)