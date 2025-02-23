# Desk Setup Version Manager

デスク周りの機材やアイテムを管理し、その配置やセットアップのバージョンを記録するためのCLIツールです。

## 機能

- デスクアイテムの登録と一覧表示
- デスク環境のバージョン作成と管理
- バージョンへのアイテムの追加
- バージョン詳細の表示

## 使い方

### 事前準備
エイリアスの設定（必要な場合）
```bash
alias python=python3
source ~/.zshrc
python --version
# 以下のようにバージョンが表示されればOK
Python 3.x.x
```

### アイテムの管理

1. アイテムの登録:
```bash
python desk_cli.py create-item "アイテム名" "カテゴリ"

# 例
python desk_cli.py create-item "MacBook Pro 14inch" "PC"
python desk_cli.py create-item "Dell U2720Q" "モニタ"
```

2. アイテム一覧の表示:
```bash
python desk_cli.py list-items
```

### バージョン管理

1. 新しいバージョンの作成:
```bash
python desk_cli.py create-version "バージョン名"

# 例
python desk_cli.py create-version "在宅勤務セットアップ2024"
```

2. バージョン一覧の表示:
```bash
python desk_cli.py list-versions
```

3. バージョンへのアイテム追加:
```bash
python desk_cli.py add-item-to-version バージョンID アイテムID

# 例
python desk_cli.py add-item-to-version 1 1  # バージョン1にアイテム1を追加
```

4. バージョン詳細の表示:
```bash
python desk_cli.py show-version バージョンID

# 例
python desk_cli.py show-version 1
```

## データ保存

- アイテムデータは `items.json` に保存されます
- バージョンデータは `versions.json` に保存されます
- これらのファイルは自動的に作成・更新されます

## ヘルプの表示

各コマンドの詳細なヘルプを表示するには:

```bash
python desk_cli.py --help
python desk_cli.py <command> --help
```
