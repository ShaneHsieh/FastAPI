from fastapi.testclient import TestClient
from main import app 
import json

client = TestClient(app)

def test_default_create_supplier():
    response = client.post("/api/v1/suppliers/", json={
        "name": "Supplier A",
        "contact_info": "supplier_a@example.com",
        "rating": 3
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Supplier A"
    assert response.json()["rating"] == 3

    response = client.post("/api/v1/suppliers/", json={
        "name": "Supplier B",
        "contact_info": "Supplier_b@example.com",
        "rating": 5
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Supplier B"
    assert response.json()["rating"] == 5

def test_create_product():
    product_data = {
        "name": "Test Product",
        "price": 99.99,
        "description": "This is a test product.",
        "stock": 10,
        "category": "Electronics",
        "discount": 10,
        "suppliers": ["Supplier A", "Supplier B"]
    }
    response = client.post("/api/v1/products", json=product_data)

    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
    assert response.json()["price"] == product_data["price"]
    assert response.json()["description"] == product_data["description"]
    assert response.json()["stock"] == product_data["stock"]
    assert response.json()["category"] == product_data["category"]
    assert response.json()["discount"] == product_data["discount"]
    #assert set(response.json()["supplier_ids"]) == set(product_data["supplier_ids"])

def test_create_product_invalid_data():
    invalid_product_data = {
        "name": "Te",  # 名稱少於 3 字符
        "price": -10,  # 價格為負數
        "stock": -5,  # 庫存為負數
        "discount": 150  # 折扣超過 100%
    }
    response = client.post("/api/v1/products", json=invalid_product_data)

    assert response.status_code == 422  

def test_get_product():
    response = client.get("/api/v1/products/1")  

    assert response.status_code == 200
    assert "name" in response.json()
    assert "price" in response.json()
    assert "description" in response.json()
    assert "stock" in response.json()
    assert "category" in response.json()
    assert "discount" in response.json()
    #assert "suppliers" in response.json()
    assert "created_at" in response.json()
    assert "updated_at" in response.json()

def test_update_product():
    product_id = 1
    updated_data = {
        "id": product_id,
        "name": "Updated Product",
        "price": 120.0,
        "description": "Updated description.",
        "stock": 50,
        "category": "Updated Category",
        "discount": 15
    }
    response = client.put(f"/api/v1/products/{product_id}", json=updated_data)

    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == updated_data["name"]
    assert updated_product["price"] == updated_data["price"]
    assert updated_product["description"] == updated_data["description"]
    assert updated_product["stock"] == updated_data["stock"]
    assert updated_product["category"] == updated_data["category"]
    assert updated_product["discount"] == updated_data["discount"]

def test_get_products():
    response = client.get("/api/v1/products/")  

    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0 
    for product in products:
        print(product)
        assert "name" in product
        assert "price" in product
        assert "description" in product
        assert "stock" in product
        assert "category" in product
        assert "discount" in product
        #assert "suppliers" in product
        assert "created_at" in product
        assert "updated_at" in product

def test_create_supplier():
    response = client.post("/api/v1/suppliers/", json={
        "name": "Test Supplier",
        "contact_info": "test@example.com",
        "rating": 4
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Supplier"
    assert response.json()["rating"] == 4

def test_get_supplier():
    supplier_id = 1
    response = client.get(f"/api/v1/suppliers/{supplier_id}")
    assert response.status_code == 200
    assert response.json()["id"] == supplier_id

def test_update_supplier():
    supplier_id = 1
    response = client.put(f"/api/v1/suppliers/{supplier_id}", json={
        "name": "Updated Supplier",
        "contact_info": "updated@example.com",
        "rating": 5
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Supplier"
    assert response.json()["rating"] == 5

# def test_delete_supplier():
#     supplier_id = 1
#     response = client.delete(f"/api/v1/suppliers/{supplier_id}")
#     print("test_delete_supplier")
#     print("Status Code:", response.status_code)
#     assert response.status_code == 204

def test_read_suppliers():
    # Act: 發送 GET 請求
    response = client.get("/api/v1/suppliers/")
    
    # Assert: 驗證回應
    assert response.status_code == 200
    
    # 驗證回應的結構和內容
    suppliers = response.json()
    assert isinstance(suppliers, list)
    assert len(suppliers) > 0  # 確保至少有一個供應商
    for supplier in suppliers:
        print(supplier)
        assert "id" in supplier
        assert "name" in supplier
        assert "contact_info" in supplier
        assert "rating" in supplier

def test_batch_create_products():
    products_data = [
        {
            "name": "Product 1",
            "price": 50.0,
            "description": "Description for Product 1",
            "stock": 20,
            "category": "Category 1",
            "discount": 5
        },
        {
            "name": "Product 2",
            "price": 75.0,
            "description": "Description for Product 2",
            "stock": 15,
            "category": "Category 2",
            "discount": 10
        },
        {
            "name": "Product 3",
            "price": 100.0,
            "description": "Description for Product 3",
            "stock": 1,
            "category": "Category 3",
            "discount": 10
        },
        {
            "name": "Product 4",
            "price": 1.0,
            "description": "Description for Product 4",
            "stock": 2,
            "category": "Category 4",
            "discount": 10
        }
    ]
    response = client.post("/api/v1/products/batch", json=products_data)

    assert response.status_code == 201
    assert len(response.json()) == len(products_data)
    for product, data in zip(response.json(), products_data):
        assert product["name"] == data["name"]
        assert product["price"] == data["price"]

def test_batch_update_products():
    updates = [
        {"id": 1, "price": 30.0, "stock": 25},
        {"id": 2, "price": 80.0, "stock": 10},
        {"id": 3, "price": 60.0, "stock": 25},
        {"id": 4, "price": 80.0, "stock": 10}
    ]
    response = client.put("/api/v1/products/batch", json=updates)

    assert response.status_code == 200
    for update in updates:
        updated_product = next((p for p in response.json() if p["id"] == update["id"]), None)
        assert updated_product is not None
        assert updated_product["price"] == update["price"]
        assert updated_product["stock"] == update["stock"]

# def test_batch_delete_products():
#     product_ids = [29 , 30]
#     ids_str = ",".join(map(str, product_ids))  
#     response = client.delete(f"/api/v1/products/batch?ids={ids_str}") 

#     print("test_batch_delete_products")
#     print("Status Code:", response.status_code)
#     assert response.status_code == 204

#     # Verify products are deleted
#     for product_id in product_ids:
#         response = client.get(f"/api/v1/products/{product_id}")
#         assert response.status_code == 404

def test_read_product_history():
    product_id = 1
    start_time = "2025-01-01T00:00:00"
    end_time = "2025-12-31T23:59:59"
    response = client.get(f"/api/v1/products/{product_id}/history", params={"start_time": start_time, "end_time": end_time})

    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    for record in history:
        assert "product_id" in record
        assert "timestamp" in record
        assert "stock" in record
        assert "price" in record
