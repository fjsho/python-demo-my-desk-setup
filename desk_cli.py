#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import argparse
from datetime import datetime

# ファイルパスの定数を現在のスクリプトからの相対パスで指定
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_FILE = os.path.join(SCRIPT_DIR, "items.json")
VERSIONS_FILE = os.path.join(SCRIPT_DIR, "versions.json")

def load_json(filepath):
    """JSONファイルを読み込む。ファイルが存在しない場合はファイルを新規作成する。"""
    try:
        if not os.path.exists(filepath):
            print(f"Creating new file: {filepath}")
            # 空のリストを書き込んで初期化
            save_json(filepath, [])
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading {filepath}: {str(e)}")
        return []

def save_json(filepath, data):
    """JSONファイルに書き込む。"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Error saving {filepath}: {str(e)}")

def get_next_id(data_list):
    """データリストの中で使用されている最大IDをもとに、次のID値を返す。"""
    if not data_list:
        return 1
    return max(item["id"] for item in data_list) + 1

def create_item(name, category):
    """デスクアイテムを新規作成。"""
    if not name or not category:
        print("Error: Name and category cannot be empty")
        return
    items = load_json(ITEMS_FILE)
    new_id = get_next_id(items)
    new_item = {
        "id": new_id,
        "name": name,
        "category": category
    }
    items.append(new_item)
    save_json(ITEMS_FILE, items)
    print(f"Item created: {new_item}")

def list_items():
    """デスクアイテムを一覧表示。"""
    items = load_json(ITEMS_FILE)
    if not items:
        print("No items found.")
        return
    for item in items:
        print(f"ID: {item['id']} | name: {item['name']} | category: {item['category']}")

def create_version(version_name):
    """デスク環境のバージョンを新規作成。"""
    versions = load_json(VERSIONS_FILE)
    new_id = get_next_id(versions)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    new_version = {
        "id": new_id,
        "versionName": version_name,
        "createdAt": now,
        "items": []
    }
    versions.append(new_version)
    save_json(VERSIONS_FILE, versions)
    print(f"Version created: {new_version}")

def list_versions():
    """デスク環境のバージョンを一覧表示。"""
    versions = load_json(VERSIONS_FILE)
    if not versions:
        print("No versions found.")
        return
    for v in versions:
        print(f"ID: {v['id']} | versionName: {v['versionName']} | createdAt: {v['createdAt']} | items: {v['items']}")

def add_item_to_version(version_id, item_id):
    """指定したバージョンにアイテムを追加。"""
    if version_id < 1 or item_id < 1:
        print("Error: Invalid ID values")
        return
    versions = load_json(VERSIONS_FILE)
    items = load_json(ITEMS_FILE)

    # 該当のversionを探す
    version = next((v for v in versions if v["id"] == version_id), None)
    if version is None:
        print(f"Version ID {version_id} not found.")
        return

    # 該当のitemを探す
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        print(f"Item ID {item_id} not found.")
        return

    # 既に追加済みでないかチェック
    if item_id in version["items"]:
        print(f"Item ID {item_id} is already in Version ID {version_id}.")
        return

    version["items"].append(item_id)
    save_json(VERSIONS_FILE, versions)
    print(f"Added Item {item_id} to Version {version_id}.")

def show_version(version_id):
    """指定したバージョンの詳細を表示（含まれるアイテムもまとめて表示）。"""
    versions = load_json(VERSIONS_FILE)
    items = load_json(ITEMS_FILE)

    version = next((v for v in versions if v["id"] == version_id), None)
    if version is None:
        print(f"Version ID {version_id} not found.")
        return

    print(f"Version ID: {version['id']}")
    print(f"versionName: {version['versionName']}")
    print(f"createdAt: {version['createdAt']}")
    print("Items:")
    for i_id in version["items"]:
        item = next((i for i in items if i["id"] == i_id), None)
        if item:
            print(f"  - {item['id']}: {item['name']} ({item['category']})")
        else:
            print(f"  - {i_id}: [Item not found in items.json]")

def main():
    parser = argparse.ArgumentParser(description="Desk environment version management CLI.")
    subparsers = parser.add_subparsers(dest="command")

    # create-item
    parser_create_item = subparsers.add_parser("create-item", help="Create a new desk item.")
    parser_create_item.add_argument("name", type=str, help="Item name.")
    parser_create_item.add_argument("category", type=str, help="Item category.")

    # list-items
    parser_list_items = subparsers.add_parser("list-items", help="List all desk items.")

    # create-version
    parser_create_version = subparsers.add_parser("create-version", help="Create a new desk environment version.")
    parser_create_version.add_argument("versionName", type=str, help="Version name.")

    # list-versions
    parser_list_versions = subparsers.add_parser("list-versions", help="List all versions.")

    # add-item-to-version
    parser_add_item_to_version = subparsers.add_parser("add-item-to-version", help="Add an item to a version.")
    parser_add_item_to_version.add_argument("versionId", type=int, help="Version ID.")
    parser_add_item_to_version.add_argument("itemId", type=int, help="Item ID.")

    # show-version
    parser_show_version = subparsers.add_parser("show-version", help="Show version details.")
    parser_show_version.add_argument("versionId", type=int, help="Version ID.")

    args = parser.parse_args()

    if args.command == "create-item":
        create_item(args.name, args.category)
    elif args.command == "list-items":
        list_items()
    elif args.command == "create-version":
        create_version(args.versionName)
    elif args.command == "list-versions":
        list_versions()
    elif args.command == "add-item-to-version":
        add_item_to_version(args.versionId, args.itemId)
    elif args.command == "show-version":
        show_version(args.versionId)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
