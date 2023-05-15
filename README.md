# 我不是機器人

## 目次

- [介紹](#介紹)
- [指令](#指令)
- [環境變數](#環境變數)

## 介紹

我不是機器人 是 LINE Messaging API 部屬在 Vercel 上尚開發的應用程式。透過安裝步驟，你可以立即使用 LINE 手機應用程式與之聊天。

## 指令

### 一般指令
指令 | 說明
--- | ---
`!hello` | 可喚醒機器人
`!quite` | 靜音模式
`!今(明)天XX市(縣)XX區(鄉、鎮、市)天氣` |提供該縣市的天氣預報
`!img + 指令` | 提供該指令圖片
`/ + 指令` | 提供該指令問結果 
`!whoami` | 可確認自己身分

### 查詢指令
指令 | 說明
--- | ---
`!introduce` | 可查看所有指令

## 環境變數
請於 Vercel 平台設置環境變數

名稱 | 說明
--- | ---
`LINE_CHANNEL_ACCESS_TOKEN` | LINE 的 [channel access token]
`LINE_CHANNEL_SECRET` | LINE 的 [channel secret]
`weather_api` | 中央氣象局的 的 [API]
`line_notify_token` | LINE 的 [notify_API]
`Open_api` | OpenAI 的 [API]
