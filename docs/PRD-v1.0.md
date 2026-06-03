# Pigeon AI（和平鴿智慧體）PRD v1.0

## 一、產品定位

### 產品名稱

- 中文：和平鴿智慧體
- 英文：Pigeon AI

### 產品願景

打造台灣第一套結合 AI 智慧助理、鴿舍管理、血統分析、競翔管理、知識庫與產業資訊平台的全功能賽鴿生態系統。

### 目標客群

1. 台灣職業賽鴿家
2. 業餘賽鴿家
3. 種鴿育種者
4. 鴿會管理人員
5. 鴿藥及飼料供應商
6. 國際賽鴿玩家

### 支援平台

- Android
- iPhone (iOS)
- Web Admin 後台

---

## 二、技術架構

### Frontend

Flutter

原因：

- 一套程式碼同時支援 Android/iOS
- 開發成本最低
- UI 一致性高

### Backend

NestJS

### Database

PostgreSQL

### Cache

Redis

### Storage

AWS S3

### AI Service

- OpenAI GPT
- OpenAI Vision
- Whisper STT

### Push Service

Firebase Cloud Messaging

### Authentication

- Email OTP
- Google Login
- Apple Login
- LINE Login

---

## 三、核心模組

## 模組 A：AI 智慧助理

代號：AI Pigeon Assistant

### A01 語音對話

支援：

- 國語
- 台語

流程：

1. 使用者按下麥克風
2. Whisper 辨識
3. GPT 理解
4. 語音回覆

### A02 圖片分析

上傳：

- 賽鴿照片
- 血統書
- 成績單
- 投注表
- 鴿眼照片
- 羽翼照片

AI 輸出：

- OCR 文字
- 表格
- PDF
- 摘要

### A03 Excel 分析

支援：

- xls
- xlsx
- csv

分析內容：

- 血統統計
- 得獎率分析
- 育種分析

### A04 AI 血統分析

輸入：環號

輸出：

- 祖代關係圖
- 近親係數
- 優勢血統
- 推薦配對

### A05 AI 問答

知識庫來源：

- 賽鴿百科
- 醫療知識
- 育種知識
- 競翔知識
- 用戶個人鴿舍資料

---

## 模組 B：我的鴿舍

### B01 鴿子主檔

唯一識別：Ring Number

資料：

- 環號
- 性別
- 羽色
- 出生日期
- 父環號
- 母環號
- 照片

### B02 血統書管理

支援：

- 3 代
- 5 代
- 7 代

輸出：

- PDF
- 樹狀圖

### B03 配種管理

紀錄：

- 公鴿
- 母鴿
- 配種日期
- 成功日期
- 產蛋日期
- 孵化日期
- 掛環日期

### B04 健康管理

- 預防保健
- 營養補充
- 治療紀錄
- 死亡紀錄
- 藥品紀錄

附件：

- 照片
- 病歷
- PDF

### B05 比賽管理

紀錄：

- 賽季
- 鴿會
- 關別
- 日期
- 天氣
- 名次
- 分速
- 獎金
- 綜合排名

---

## 模組 C：AI 育種中心

目的：建立台灣第一套賽鴿育種推薦系統

### 配對推薦

輸入：

- 公鴿 A
- 母鴿 B

輸出：

- 育種評分
- 成功率
- 優勢基因
- 風險警示

### 血統交叉分析

分析：

- 同血系比例
- 近親程度
- 歷代成績
- 推薦配對名單

---

## 模組 D：競翔中心

功能：

- 鴿會管理
- 賽程管理
- 成績管理
- 積分排名
- 賽季統計

---

## 模組 E：即時中心

整合：

- Windy
- 中央氣象署

功能：

- 即時風向
- 風速
- 溫度
- 降雨
- 海象
- 飛行風險評估

---

## 模組 F：賽鴿知識庫

分類：

- 銘鴿資料庫
- 世界強豪資料庫
- 國際賽事資料庫
- 鴿病百科
- 飼料百科
- 用藥百科

---

## 模組 G：產業導航

內容：

- 台灣鴿會
- 鴿店
- 獸醫院
- DNA 檢測中心
- 拍賣網站
- 國際賽事網站

---

## 四、資料庫設計

### Users

- user_id
- name
- phone
- email
- role
- created_at

### Pigeons

- pigeon_id
- ring_number
- name
- gender
- father_ring
- mother_ring
- birth_date
- color
- status
- photo_url

### Pedigrees

- pedigree_id
- pigeon_id
- generation
- father_id
- mother_id

### HealthRecords

- record_id
- pigeon_id
- type
- medicine
- symptom
- result
- created_at

### RaceRecords

- record_id
- pigeon_id
- club
- race_name
- race_date
- weather
- rank
- speed
- prize

### BreedingRecords

- record_id
- male_id
- female_id
- breed_date
- egg_date
- hatch_date
- ring_date

### AIAnalysis

- analysis_id
- pigeon_id
- analysis_type
- result_json
- created_at

---

## 五、管理後台

- 會員管理
- 鴿舍管理
- 公告管理
- 賽事管理
- 廣告管理
- 知識庫管理
- AI Token 監控
- 營運報表

---

## 六、會員制度

### 免費會員

- 100 次 AI/月

### VIP 會員

- 無限制 AI 分析
- 雲端備份
- 高級血統分析

### 企業會員

- 多鴿舍
- 團隊帳號
- API 介接

---

## 七、MVP 版本

第一階段：

1. AI 聊天
2. 鴿舍管理
3. 血統書管理
4. 健康管理
5. 比賽管理
6. 雲端同步

預估：12~16 週

---

## 八、V2 版本

1. AI 育種推薦
2. AI 鴿眼分析
3. AI 羽翼分析
4. AI 競翔預測
5. AI 疾病預警
6. 社群系統

---

## 九、V3 版本

1. 鴿舍 IoT 整合
2. 智慧感測器
3. AI 數位分身
4. 國際賽事平台
5. NFT 血統認證
6. 區塊鏈血統書

---

## 十、成功指標（KPI）

首年目標：

- 註冊會員 10,000+
- 付費會員 1,000+
- 建檔賽鴿 100,000 羽+
- AI 分析次數 500 萬次+
- 成為台灣最大賽鴿 AI 平台
