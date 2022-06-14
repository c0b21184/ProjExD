import random
def main():
    seikai = syutudai()
    kaitou(seikai)
def syutudai():
    quiz = [
        {"q":"サザエの旦那の名前は？","a":["マスオ","ますお"]},
        {"q":"カツオの妹の名前は？","a":["ワカメ","わかめ"]},
        {"q":"タラオはカツオから見てどんな関係？","a":["甥","おい","甥っ子","おいっこ"]}
        ]
    print("問題:")
    r = random.randint(0,2)
    print(quiz[r]["q"])
    return quiz[r]["a"]

def kaitou(seikai):
    ans = input("答え:")
    if(ans in seikai):
        print("正解")
    else:
        print("不正解")

if __name__ == "__main__":
    main()