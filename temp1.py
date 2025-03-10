# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from flask import Flask, render_template
import random
import pymysql


import serial
import re
import time

ser = serial.Serial('COM5', 115200)  # 將 'COMx' 替換為您的串口號
captured = False
start_time = time.time()

while not captured and time.time() - start_time < 5:
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        print(f"Received data: {data}")
        numbers = re.findall(r'\d+', data)  # 使用正則表達式匹配字串中的數字部分

        # 將提取到的數字部分合併為一個數字
        combined_number = int(''.join(numbers))

        print(combined_number)  # 印出合併後的數字
        captured = True

ser.close()  # 關閉串口連接

random.seed(combined_number)

app = Flask(_name_)
app = Flask(_name_, static_url_path='/static')






# 百家樂遊戲類別
class Baccarat:
    def __init__(self):
        self.deck = self.generate_deck()
        self.player_score = 0
        self.banker_score = 0
        

    # 生成一副牌
    def generate_deck(self):
        deck = []
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        for suit in suits:
            for rank in ranks:
                deck.append(rank + suit)
        
        random.shuffle(deck)
        return deck

    # 發牌
    def deal_card(self):
        card = self.deck.pop() #最後
        return card

    # 計算牌值
    def calculate_score(self, hand):
        score = 0
        for card in hand:
            rank = card[:-1]
            if rank.isdigit():
                score += int(rank)
            elif rank == 'A':
                score += 1
            else:
                score += 10
        return score % 10

    # 遊戲流程
    def play(self):
        # 開始發牌
        player_hand = [self.deal_card(), self.deal_card()]
        banker_hand = [self.deal_card(), self.deal_card()]

        # 計算牌值
        self.player_score = self.calculate_score(player_hand)
        self.banker_score = self.calculate_score(banker_hand)
        
        if self.player_score >= 8 and self.banker_score < 8:
            self.player_score = self.calculate_score(player_hand)
            self.banker_score = self.calculate_score(banker_hand)
            
        # 檢查是否需要補牌
        if self.banker_score < 6 and self.player_score < 8:
            banker_hand.append(self.deal_card())
            self.banker_score = self.calculate_score(banker_hand)
        
        if self.player_score < 6 and self.banker_score < 8:
            player_hand.append(self.deal_card())
            self.player_score = self.calculate_score(player_hand)
            

        # 判斷勝負
        if self.player_score > self.banker_score:
            result = "Player wins!"
        elif self.player_score < self.banker_score:
            result = "Banker wins!"
        else:
            result = "It's a tie!"

        # 回傳結果
        return {
            'player_hand': player_hand,
            'banker_hand': banker_hand,
            'player_score': self.player_score,
            'banker_score': self.banker_score,
            'result': result
        }

# 測試遊戲
game = Baccarat()
result = game.play()

# 顯示結果
print("Player's Hand:", result['player_hand'])
print("Banker's Hand:", result['banker_hand'])
print("Player's Score:", result['player_score'])
print("Banker's Score:", result['banker_score'])
print("Result:", result['result'])
hand_numbers = [card[:-1] for card in result['player_hand']]
print("Player's Hand:", ', '.join(hand_numbers))






# 定義路由及處理函式
@app.route("/")
def play_baccarat():
    # 測試遊戲
    game = Baccarat()
    result = game.play()
    #p
    phand1 = result['player_hand'][0]
    image_path = f"pokers/{phand1}.jpg"
    phand2 = result['player_hand'][1]
    image_path2 = f"pokers/{phand2}.jpg"
    if len(result['player_hand']) >= 3:
        phand3 = result['player_hand'][2]
        image_path3 = f"pokers/{phand3}.jpg"
    else:
        image_path3 = f"pokers/{0}.jpg"
    #b
    bhand1 = result['banker_hand'][0]
    image_path4 = f"pokers/{bhand1}.jpg"
    bhand2 = result['banker_hand'][1]
    image_path5 = f"pokers/{bhand2}.jpg"
    if len(result['banker_hand']) >= 3:
        bhand3 = result['banker_hand'][2]
        image_path6 = f"pokers/{bhand3}.jpg"
    else:
        image_path6 = f"pokers/{0}.jpg"
    

    

    try:
        db = pymysql.connect(host='127.0.0.1', port=3306, password='2204', user='ttlee', db='baccarat', charset='utf8')
        cursor = db.cursor()

    # 執行 INSERT 的 SQL 語句，使用轉義後的 result['result'] 值插入
        insert_query = f"INSERT INTO game (time, p, b, result) VALUES (NOW(), '{result['player_score']}', '{result['banker_score']}', '{result['result']}')"
        cursor.execute(insert_query)

        db.commit()
        print('Records created successfully!')
    except Exception as e:
        print(f"Encounter exception: {e}")
        db.rollback()
    finally:
    # 斷開資料庫的連線
        db.close()

        
    

    # 回傳結果至模板
    return render_template('baccarat.html', result=result,image_path=image_path,image_path2=image_path2,image_path3=image_path3,image_path4=image_path4,image_path5=image_path5,image_path6=image_path6)

@app.route("/game_results")
def game_results():
    try:
        db = pymysql.connect(host='127.0.0.1', port=3306, password='', user='root', db='baccarat', charset='utf8')
        cursor = db.cursor()

        # 執行 SQL 查詢
        with db.cursor() as cursor:
            sql = "SELECT * FROM game"
            cursor.execute(sql)
            result = cursor.fetchall()

      
            
   

    except Exception as e:
        return str(e)
    finally:
        # 關閉資料庫連線
        db.close()
        return render_template('game_results.html', result=result)


if _name_ == '_main_':
    app.run()
