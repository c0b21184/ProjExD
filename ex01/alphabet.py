import random
import datetime

NUM_OF_TRIALS = 5
NUM_OF_ALL_CHARS = 10
NUM_OF_ABS_CHARS = 2

def main():
    st = datetime.datetime.now() #計測開始
    for _ in range(NUM_OF_TRIALS):
        seikai = syutudai()
        f = kaitou(seikai)
        if (f == 1):
            break
    ed = datetime.datetime.now() #計測終了
    print((ed-st).second,"秒")

def syutudai():
    alphabets = [chr(c + 65) for c in range(26)]
    all_char_lst = random.sample(alphabets , NUM_OF_ALL_CHARS)
    print("対象文字:",all_char_lst)

    abs_char_lst = random.sample(all_char_lst , NUM_OF_ABS_CHARS)
    print("欠損文字:",abs_char_lst)

    pre_char_lst = [c for c in all_char_lst if c not in abs_char_lst]
    print("表示文字:",pre_char_lst)

    return abs_char_lst

def kaitou(seikai):
    num = int(input("欠損文字はいくつ?"))
    if (num != NUM_OF_ABS_CHARS):
        print("不正解")
        return 0
    else:
        print("正解。具体的には?")
        for i in range(NUM_OF_ABS_CHARS):
            c = input(i+1,"つ目の文字を入力してください")
            if c not in seikai:
                print("不正解")
                return 0
            seikai.remove(c)
        print("正解")
        return 1

if __name__ == "__main__":
    main()