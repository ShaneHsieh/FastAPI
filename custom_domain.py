import httpx
import json
import argparse

def test_with_custom_domain(domain: str):
    client = httpx.Client(base_url=domain, follow_redirects=True)  # 啟用自動跟隨重定向

    def test_create_product():
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "description": "This is a test product.",
            "stock": 10,
            "category": "Electronics",
            "discount": 10
        }
        response = client.post("/api/v1/products/", json=product_data)  # 確保路徑以 '/' 結尾
        print(response.status_code)
        print(response.headers.get("location"))  # 查看重定向位置（如果有）

        assert response.status_code == 201
        assert response.json()["name"] == product_data["name"]
        assert response.json()["price"] == product_data["price"]

    def test_get_product():
        product_id = 1
        response = client.get(f"/api/v1/products/{product_id}")  # 發送 GET 請求

        assert response.status_code == 200
        assert "name" in response.json()
        assert "price" in response.json()

    print("Running tests with custom domain...")
    # Add more tests as needed
    test_create_product()
    test_get_product()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests with a custom domain.")
    parser.add_argument("--domain", type=str, required=True, help="The custom domain to test against.")
    args = parser.parse_args()

    test_with_custom_domain(args.domain)
