# 計算理論專題 F74041103 趙哲宏
## 主要功能
* 實行文字冒險遊戲
* 部分回應輸入的話，以及一點小彩蛋
## 執行方式
* 在目錄下，執行**python3 bot.py**，顯示You can start now後可開始傳送資訊
## state表示圖
[picture]: https://raw.githubusercontent.com/shuuennokage/CTProject/master/state_diagram.png  "pic"
![Alt text][picture]
## state說明
* 共有5個state，分別滿足條件後會trigger至其他state(詳細於code中)
* 除了初始state，有分別設置on enter函式，供debug訊息顯示(確認state移動)
## 遊戲進行方式
* 可先輸入/start或任意字串符，會顯示提示訊息
* 輸入start後，遊戲開始，會隨機為勇者分配數值
* 遊戲開始後，文本會開始發送，可以隨指令輸入，推進遊戲進度
* 輸入要求以外的文字，會有額外的一點文本演出或是小彩蛋
> 備註: 因使用getUpdates方法，在polling的時候有機率發生timeOut，敬請見諒
