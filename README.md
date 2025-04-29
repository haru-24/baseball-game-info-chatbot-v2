# Baseball Chatbot V2

※ この README は Claude が書きました。

野球情報を提供する LINE チャットボットです。犬になりきって、最新の野球試合結果や情報をお届けします。

## 機能

- 本日の日本プロ野球の試合結果を自動取得
- 野球に関する質問に回答
- LINE プラットフォームを通じたコミュニケーション
- パグキャラクターとしての会話体験

## 技術スタック

- **バックエンド**: FastAPI, Python 3.12
- **AI**: LangChain, OpenAI GPT-4o-mini
- **スクレイピング**: BeautifulSoup4, Requests
- **メッセージング**: LINE Bot SDK
- **デプロイ**: Docker, Google Cloud Run

## 開発環境のセットアップ

### 前提条件

- Python 3.12
- Docker と Docker Compose
- LINE Developer アカウント
- OpenAI API キー

### 環境変数

`.env` ファイルを作成し、以下の変数を設定してください：

```
OPENAI_API_KEY=your_openai_api_key
CHANNEL_SECRET=your_line_channel_secret
CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
```

### Docker を使った起動方法

```bash
docker-compose up --build
```

アプリケーションは `http://localhost:8000` で実行されます。

### API エンドポイント

- `GET /`: Hello World!
- `POST /webhook`: LINE Webhook
- `POST /talk`: AI との直接会話用エンドポイント

## LINE Bot の設定

1. [LINE Developers Console](https://developers.line.biz/) でチャネルを作成
2. Webhook URL を設定: `https://your-domain.com/webhook`
3. チャネルシークレットとアクセストークンを `.env` ファイルに設定
