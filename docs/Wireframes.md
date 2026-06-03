# Pigeon AI Wireframes

## 1. Purpose

This Phase 1 document provides low-fidelity wireframes for review. It is not final visual design and contains no application source code.

## 2. Mobile Wireframe Conventions

- Traditional Chinese labels are shown for primary UI.
- Primary actions are large and placed near the bottom where practical.
- Ring Number is emphasized as the main pigeon identifier.
- Voice input is represented by `🎤`.

## 3. Mobile Screens

### 3.1 Login

```text
┌─────────────────────────────┐
│ 和平鴿智慧體                 │
│ Pigeon AI                   │
│                             │
│ 手機 / Email                │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ └─────────────────────────┘ │
│ 密碼                        │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ └─────────────────────────┘ │
│                             │
│ [ 大按鈕：登入 ]             │
│ [ 註冊新帳號 ] [ 忘記密碼 ]  │
│                             │
│ 語言：繁體中文              │
└─────────────────────────────┘
```

### 3.2 Home Dashboard

```text
┌─────────────────────────────┐
│ 早安，王先生                 │
│ 今日提醒：3 件               │
├─────────────────────────────┤
│ [搜尋鴿環號碼____________ 🎤] │
├─────────────────────────────┤
│ 快速功能                     │
│ [新增鴿子] [健康紀錄]        │
│ [AI 助手] [天氣中心]         │
├─────────────────────────────┤
│ 今日天氣                     │
│ 風向：東北  溫度：24°C       │
│ 放飛建議：注意側風           │
├─────────────────────────────┤
│ 首頁 | 鴿舍 | 比賽 | AI | 我的│
└─────────────────────────────┘
```

### 3.3 Loft/Pigeon List

```text
┌─────────────────────────────┐
│ 鴿舍                         │
│ [搜尋鴿環號碼___________ 🎤]  │
│ [＋ 新增鴿子]                │
├─────────────────────────────┤
│ TW-2025-001234               │
│ 公 / 灰 / 狀態：健康          │
│ [查看] [新增紀錄]            │
├─────────────────────────────┤
│ TW-2025-001235               │
│ 母 / 斑 / 狀態：訓練中        │
│ [查看] [新增紀錄]            │
└─────────────────────────────┘
```

### 3.4 Register Pigeon

```text
┌─────────────────────────────┐
│ 新增鴿子                     │
│ 鴿環號碼 *                   │
│ ┌─────────────────────────┐ │
│ │ TW-2026-______          │ │
│ └─────────────────────────┘ │
│ 名稱 / 暱稱                  │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ └─────────────────────────┘ │
│ 性別 [未知 ▼]  羽色 [選擇 ▼] │
│ 出生日期 [選擇日期]          │
│ [拍照或上傳照片]             │
│                             │
│ [ 大按鈕：儲存 ]             │
└─────────────────────────────┘
```

### 3.5 Pigeon Profile

```text
┌─────────────────────────────┐
│ TW-2025-001234               │
│ [照片]  公 / 灰 / 健康        │
│ 鴿舍：和平鴿舍               │
├─────────────────────────────┤
│ [AI 分析] [新增健康]          │
│ [血統] [比賽成績]             │
├─────────────────────────────┤
│ 時間軸                       │
│ 06/01 健康：接種疫苗          │
│ 05/20 訓練：30km              │
│ 05/02 比賽：第 12 名          │
└─────────────────────────────┘
```

### 3.6 Health Record

```text
┌─────────────────────────────┐
│ 新增健康紀錄                 │
│ 鴿環：TW-2025-001234         │
├─────────────────────────────┤
│ 症狀 / 備註                  │
│ ┌─────────────────────────┐ │
│ │ 可輸入或用語音說明...   │ │
│ └─────────────────────────┘ │
│ [🎤 語音輸入] [📷 上傳照片]   │
│ 日期 [今天 ▼]                │
│ [儲存紀錄]                   │
│ [儲存並請 AI 分析]           │
│ 提醒：AI 不能取代獸醫診斷     │
└─────────────────────────────┘
```

### 3.7 AI Assistant

```text
┌─────────────────────────────┐
│ AI 助手                      │
│ 關聯鴿環：[可選擇 ▼]          │
├─────────────────────────────┤
│ AI：您好，想查健康、血統、    │
│ 配對或比賽資訊嗎？           │
│                             │
│ 使用者：這羽最近精神不好...   │
│                             │
│ AI：根據您的紀錄，建議先...   │
│ 來源：[健康紀錄] [知識庫]     │
├─────────────────────────────┤
│ [輸入問題______________ 🎤]   │
│ [＋ 上傳照片/PDF/Excel]       │
└─────────────────────────────┘
```

### 3.8 Race Detail

```text
┌─────────────────────────────┐
│ 春季資格賽                   │
│ 放飛：新竹  距離：120km      │
├─────────────────────────────┤
│ 天氣                         │
│ 風向：東北  風速：中          │
│ 風險：中                     │
├─────────────────────────────┤
│ [登錄參賽鴿] [查看成績]       │
│ [AI 賽事分析]                │
└─────────────────────────────┘
```

## 4. Admin Wireframes

### 4.1 Admin Dashboard

```text
┌────────────────────────────────────────────────────┐
│ Pigeon AI Admin                                    │
├──────────────┬─────────────────────────────────────┤
│ Dashboard    │ 今日摘要                            │
│ Users        │ 使用者：12,340                       │
│ Pigeons      │ 鴿環數：88,210                       │
│ Races        │ AI 請求：3,420                       │
│ Knowledge    │ 系統狀態：正常                       │
│ AI Monitor   │                                     │
│ Audit Logs   │ [圖表：活躍使用者] [圖表：AI 用量]    │
└──────────────┴─────────────────────────────────────┘
```

### 4.2 User Management

```text
┌────────────────────────────────────────────────────┐
│ User Management                                    │
│ Search: [phone/email/name/ring number__________]   │
├────────────────────────────────────────────────────┤
│ Name      Phone       Plan      Status   Actions   │
│ 王先生    09xx...     Pro       Active   [View]     │
│ 李先生    09xx...     Free      Active   [View]     │
└────────────────────────────────────────────────────┘
```

### 4.3 Knowledge Management

```text
┌────────────────────────────────────────────────────┐
│ Knowledge Management                               │
│ [Upload Document] [Categories] [Review Queue]       │
├────────────────────────────────────────────────────┤
│ Title             Category   Status     Actions     │
│ 疾病預防指南       Health     Published  [Edit]      │
│ 配對育種經驗       Breeding   Draft      [Review]    │
└────────────────────────────────────────────────────┘
```

### 4.4 AI Monitoring

```text
┌────────────────────────────────────────────────────┐
│ AI Monitoring                                      │
│ Requests Today: 3,420   Error Rate: 0.8%            │
│ Token Usage: 12.4M      Avg Latency: 2.1s           │
├────────────────────────────────────────────────────┤
│ Recent Jobs                                          │
│ health_analysis  completed  TW-2025-001234          │
│ ocr_import       failed     upload_123              │
└────────────────────────────────────────────────────┘
```

## 5. Wireframe Acceptance Criteria

- Wireframes include login, home, pigeon list, pigeon registration, profile, health, AI assistant, race, and admin screens.
- Ring Number is prominent across pigeon workflows.
- Large, simple controls are reflected in layout.
- Voice and upload affordances are visible in AI and data-entry flows.
- No runnable UI source code is generated.

## 6. Architecture Notes

- Wireframes intentionally use low-fidelity text blocks to keep Phase 1 focused on information architecture rather than visual styling.
- Mobile screens emphasize large labels, obvious actions, and Ring Number search.
- Admin screens emphasize operator efficiency, auditability, and platform oversight.
- Final UI implementation in later phases should validate these layouts with older Taiwan breeder users before production release.
