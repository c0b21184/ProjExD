# 第1回
## サザエさんクイズ（ex01/quiz.py）
### 遊び方
* コマンドラインでquiz.pyを実行すると，標準出力に問題が表示される．
* 標準入力から答えを入力する．
* 正解なら「正解！！！」と表示される．
* 不正解なら「出直してこい」と表示される．
* 正解でも不正解でも，1問のみ出題される．
### プログラム内の解説
* main関数：クイズプログラムの全体の流れを担当する．
* shutudai関数：ランダムに選んだ問題を出題し，解答をmain関数に返す．
* kaitou関数：回答と正解をチェックし，結果を出力する．

## アルファベットクイズ
### 遊び方
* コマンドラインでalphabet.pyを実行すると、問題が出力される
* 欠損しているアルファベットの答えを入力→正解で次へ、不正解でもう一度、最大５回繰り返す
* 欠損しているアルファベットを答えるとクリア。正解までの時間を出力

###　プログラム内の解説
* main :全体の流れ、時間計測
* syutudai :アルファベットのリストと欠損しているアルファベットのリストを出力
* kaitou :回答と正解をチェックし、結果を出力