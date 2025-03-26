from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_default_create_supplier():
    response = client.post("/api/v1/suppliers/", json={
        "name": "Supplier A",
        "contact_info": "supplier_a@example.com",
        "rating": 3
    })
    print("default_create_supplier")
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 201
    assert response.json()["name"] == "Supplier A"
    assert response.json()["rating"] == 3

    response = client.post("/api/v1/suppliers/", json={
        "name": "Supplier B",
        "contact_info": "Supplier_b@example.com",
        "rating": 5
    })

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
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

    print("test_create_product")
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
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

    print("test_create_product_invalid_data")
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 422  

def test_get_product():

    response = client.get("/api/v1/products/1")  

    print("test_get_product")
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
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

def test_delete_supplier():
    supplier_id = 1
    response = client.delete(f"/api/v1/suppliers/{supplier_id}")
    print("test_delete_supplier")
    print("Status Code:", response.status_code)
    assert response.status_code == 204

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
