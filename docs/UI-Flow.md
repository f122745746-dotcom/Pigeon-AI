# Pigeon AI UI Flow Architecture

## 1. Purpose

This Phase 1 document defines mobile and web admin user flows for Pigeon AI. It is design architecture only and contains no Flutter or web source code.

## 2. UX Principles

Pigeon AI serves Taiwan racing pigeon breeders, many of whom are age 40-80+. The UX must prioritize clarity and low learning curve.

- Traditional Chinese first (`zh-Hant-TW`).
- Large fonts and large tap targets.
- Simple bottom navigation and clear labels.
- Voice-friendly input for notes, AI assistant, search, and health/race updates.
- Minimal form complexity per screen.
- Confirmation screens for destructive or sensitive actions.
- Ring Number-first search and lookup.
- AI assistance available contextually but never forced.

## 3. Mobile Information Architecture

Primary bottom navigation:

1. **首頁** Home
2. **鴿舍** Loft/Pigeons
3. **比賽** Race
4. **AI 助手** AI Assistant
5. **我的** Profile

Secondary feature entry cards on Home:

- 健康管理
- 配對育種
- 血統管理
- 天氣中心
- 知識庫
- 通知提醒

## 4. Mobile Primary Flows

### 4.1 First Launch and Authentication

```mermaid
flowchart TD
  Start[開啟 App] --> Locale[繁中預設 / 字體大小確認]
  Locale --> LoginChoice[登入 / 註冊]
  LoginChoice --> Register[手機或 Email 註冊]
  LoginChoice --> Login[登入]
  Register --> Onboarding[簡短導覽]
  Login --> Home[首頁儀表板]
  Onboarding --> Home
```

Requirements:

- Login screen uses large fields and high contrast.
- Voice is introduced as an optional convenience.
- Onboarding should be skippable and no more than 3-4 screens.

### 4.2 Register Pigeon by Ring Number

```mermaid
flowchart TD
  Home[首頁] --> Loft[鴿舍]
  Loft --> Add[新增鴿子]
  Add --> Ring[輸入鴿環號碼]
  Ring --> Details[基本資料]
  Details --> Photo[拍照 / 上傳照片]
  Photo --> Confirm[確認資料]
  Confirm --> Profile[鴿子資料頁]
```

Requirements:

- Ring Number is the first field.
- Duplicate Ring Number conflicts explain ownership/import options.
- Photo upload supports AI vision in later phases.

### 4.3 Pigeon Timeline

```mermaid
flowchart TD
  Search[搜尋鴿環號碼] --> Profile[鴿子資料]
  Profile --> Timeline[時間軸]
  Timeline --> Health[健康紀錄]
  Timeline --> Race[比賽成績]
  Timeline --> Breeding[配對育種]
  Timeline --> Pedigree[血統]
  Timeline --> AI[AI 分析]
```

Requirements:

- Timeline groups records by date and category.
- Primary actions are visible: 新增健康, 新增比賽, 詢問 AI.

### 4.4 Health Record with AI Assistance

```mermaid
flowchart TD
  Profile[鴿子資料] --> AddHealth[新增健康紀錄]
  AddHealth --> Input[文字 / 語音 / 照片]
  Input --> Save[儲存紀錄]
  Save --> AskAI{需要 AI 分析?}
  AskAI -->|是| AIJob[送出分析]
  AskAI -->|否| Done[完成]
  AIJob --> Result[分析結果與提醒]
  Result --> Vet[必要時建議尋求獸醫]
```

Requirements:

- AI health output must show uncertainty and veterinary escalation language.
- User can save raw record without AI.

### 4.5 AI Assistant

```mermaid
flowchart TD
  Entry[AI 助手] --> Mode[選擇: 文字 / 語音 / 上傳]
  Mode --> Context[可選鴿環號碼]
  Context --> Ask[輸入問題]
  Ask --> Retrieve[知識與個人資料檢索]
  Retrieve --> Answer[繁中回答]
  Answer --> Actions[儲存分析 / 建立提醒 / 查看來源]
```

Requirements:

- Supports Mandarin and Taiwanese Hokkien voice input where provider capabilities permit.
- User can attach Ring Number context.
- Knowledge-based answers show sources when available.

### 4.6 Race and Weather

```mermaid
flowchart TD
  RaceTab[比賽] --> Events[賽事列表]
  Events --> Detail[賽事詳情]
  Detail --> Enter[登錄參賽鴿]
  Detail --> Weather[天氣與風向]
  Detail --> Results[成績]
  Results --> Prediction[AI 賽事分析]
```

Requirements:

- Weather center uses simple icons and clear risk labels.
- Race result import correction must be reviewable before saving.

## 5. Mobile Accessibility Defaults

| Element | Target |
| --- | --- |
| Body font | At least 18sp equivalent |
| Primary action font | 20-24sp equivalent |
| Tap target | At least 48dp, preferably 56dp for primary buttons |
| Contrast | WCAG AA-aligned |
| Navigation depth | Common tasks within 2-3 taps |
| Forms | One major task per screen, save draft where useful |
| Voice | Microphone button visible on search, notes, AI assistant |

## 6. Web Admin Information Architecture

Admin portal top-level navigation:

1. Dashboard / Analytics
2. User Management
3. Pigeon and Loft Lookup
4. Race Management
5. Knowledge Management
6. Subscriptions
7. AI Monitoring
8. Notifications
9. System Monitoring
10. Audit Logs
11. Settings

## 7. Admin Primary Flows

### 7.1 User Support Flow

```mermaid
flowchart TD
  AdminLogin[Admin Login + MFA] --> SearchUser[Search User]
  SearchUser --> UserDetail[User Detail]
  UserDetail --> Membership[Membership/Entitlements]
  UserDetail --> Pigeons[Associated Ring Numbers]
  UserDetail --> Audit[Audit History]
  UserDetail --> Action[Support Action]
  Action --> Confirm[Reason + Confirmation]
  Confirm --> Logged[Audit Logged]
```

### 7.2 Knowledge Publishing Flow

```mermaid
flowchart TD
  Upload[Upload Knowledge Document] --> Metadata[Set Category/Language/Tags]
  Metadata --> Process[OCR/Chunk/Embed Job]
  Process --> Review[Editor Review]
  Review --> Publish[Publish]
  Publish --> Searchable[Available in Knowledge Search/RAG]
```

### 7.3 Race Management Flow

```mermaid
flowchart TD
  CreateRace[Create Race Event] --> Weather[Attach Weather Location]
  Weather --> Entries[Import/Manage Entries]
  Entries --> Results[Import Results]
  Results --> Validate[Validate Ring Numbers]
  Validate --> Publish[Publish Results]
  Publish --> Notify[Notify Users]
```

## 8. Notification UX

Notification categories:

- Health reminders
- Vaccination due
- Race/weather alerts
- Breeding milestones
- AI analysis complete
- Subscription/billing
- System/admin messages

Users can set preferences by channel and category. Critical account/security notifications cannot be fully disabled.

## 9. UI Acceptance Criteria

- Mobile navigation fits senior-friendly usage and Traditional Chinese terminology.
- Ring Number search and profile access are central.
- Voice input paths are included for major text flows.
- Admin portal includes user, knowledge, race, analytics, monitoring, and audit flows.
- No Flutter or web source code is generated in Phase 1.

## 10. Architecture Notes

- Mobile UX prioritizes daily breeder workflows over administrative completeness.
- AI Assistant is both a primary tab and contextual action from Ring Number pages because older users benefit from visible, repeated entry points.
- Admin UX uses dense tables only where appropriate for trained operators; breeder-facing screens should remain card-based and large-format.
- Advanced pedigree visualization can be added later, but Phase 1 flows must establish Ring Number lookup and timeline navigation first.
