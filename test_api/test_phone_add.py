"""
/api/phone/add エンドポイントのテストスクリプト
"""

import requests
import json

BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/api/phone/add"


def test_phone_add_all_params():
    """全てのパラメータを指定してテスト"""
    print("\n=== Test 1: 全パラメータ指定 ===")
    
    payload = {
        "latitude": 35.6762,
        "longitude": 139.6503,
        "battery_level": 0.85,
        "free_storage": 256,
    }
    
    try:
        response = requests.post(ENDPOINT, json=payload)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}")
    except Exception as e:
        print(f"エラー: {e}")


def test_phone_add_partial_params():
    """部分的なパラメータでテスト"""
    print("\n=== Test 2: 部分的なパラメータ ===")
    
    payload = {
        "latitude": 35.6762,
        "battery_level": 0.50,
    }
    
    try:
        response = requests.post(ENDPOINT, json=payload)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}")
    except Exception as e:
        print(f"エラー: {e}")


def test_phone_add_empty():
    """パラメータなしでテスト"""
    print("\n=== Test 3: パラメータなし ===")
    
    payload = {}
    
    try:
        response = requests.post(ENDPOINT, json=payload)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}")
    except Exception as e:
        print(f"エラー: {e}")


def test_phone_add_invalid_types():
    """不正な型でテスト"""
    print("\n=== Test 4: 不正な型 ===")
    
    payload = {
        "latitude": "invalid",
        "longitude": "invalid",
        "battery_level": "invalid",
        "free_storage": "invalid",
    }
    
    try:
        response = requests.post(ENDPOINT, json=payload)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}")
    except Exception as e:
        print(f"エラー: {e}")


def test_phone_add_zero_values():
    """0値でテスト"""
    print("\n=== Test 5: 0値の設定 ===")
    
    payload = {
        "latitude": 0.0,
        "longitude": 0.0,
        "battery_level": 0.0,
        "free_storage": 0,
    }
    
    try:
        response = requests.post(ENDPOINT, json=payload)
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}")
    except Exception as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    print(f"テストURL: {ENDPOINT}")
    print("※ Reflexアプリケーションが http://localhost:3000 で起動していることを確認してください\n")
    
    test_phone_add_all_params()
    test_phone_add_partial_params()
    test_phone_add_empty()
    test_phone_add_invalid_types()
    test_phone_add_zero_values()
    
    print("\n=== テスト完了 ===")
