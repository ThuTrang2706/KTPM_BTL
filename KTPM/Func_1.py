# Danh sách người bán (sellers) và sản phẩm (products)
sellers = [
    {
        "seller_id": 1,
        "username": "seller_1",
        "email": "seller1@example.com",
        "password": "password1",
        "phone": "+84901234567",
        "products": [1, 2]  # ID các sản phẩm mà người bán sở hữu
    },
    {
        "seller_id": 2,
        "username": "seller_2",
        "email": "seller2@example.com",
        "password": "password2",
        "phone": "+84909876543",
        "products": [3]  # ID các sản phẩm mà người bán sở hữu
    }
]
products = [
    {
        "product_id": 1,
        "name": "Điện thoại iPhone 13",
        "price": 20000000,
        "quantity": 5,
        "seller_id": 1
    },
    {
        "product_id": 2,
        "name": "Laptop Dell XPS",
        "price": 30000000,
        "quantity": 3,
        "seller_id": 1
    },
    {
        "product_id": 3,
        "name": "Máy tính bảng iPad Air",
        "price": 15000000,
        "quantity": 7,
        "seller_id": 2
    }
]

# 1. Hàm đăng ký người bán
def register(username, email, password, phone):
    # Kiểm tra xem các trường có bị thiếu không
    if not username or not password or not phone:
        return 1  # Mã lỗi: Thiếu thông tin
    
    # Kiểm tra nếu email đã tồn tại
    for seller in sellers:
        if seller['email'] == email:
            return 2  # Mã lỗi: Email đã tồn tại
    
    # Tạo người bán mới
    seller_id = len(sellers) + 1
    sellers.append({
        "seller_id": seller_id,
        "username": username,
        "email": email,
        "password": password,  # Lưu mật khẩu dưới dạng văn bản thuần
        "phone": phone,
        "products": []  # Danh sách sản phẩm của người bán
    })
    return 0  # Thành công

# 2. Hàm đăng nhập
def login(email, password):
    # Kiểm tra xem email và mật khẩu có được cung cấp không
    if not email or not password:
        return 1  # Mã lỗi: Thiếu thông tin

    for seller in sellers:
        if seller['email'] == email and seller['password'] == password:  # So sánh mật khẩu văn bản thuần
            return 0  # Thành công
    
    return 3  # Mã lỗi: Email hoặc mật khẩu không đúng

# 3. Hàm thêm sản phẩm
def add_product(seller_id, name, price, quantity):
    # Kiểm tra xem các trường có bị thiếu không
    if not name:
        return 5  # Mã lỗi: Thiếu tên sản phẩm
    if price <= 0:
        return 4  # Mã lỗi: Giá không hợp lệ
    if quantity <= 0:
        return 6  # Mã lỗi: Số lượng không hợp lệ
    
    # Kiểm tra nếu sản phẩm đã tồn tại, cập nhật số lượng
    for product in products:
        if product['name'] == name and product['seller_id'] == seller_id:
            product['quantity'] += quantity
            return 0  # Thành công, cập nhật số lượng

    # Nếu sản phẩm chưa tồn tại, tạo sản phẩm mới
    product_id = len(products) + 1
    product = {
        "product_id": product_id,
        "name": name,
        "price": price,
        "quantity": quantity,
        "seller_id": seller_id
    }
    products.append(product)
    
    # Thêm sản phẩm vào danh sách của người bán
    for seller in sellers:
        if seller["seller_id"] == seller_id:
            seller["products"].append(product)
    
    return 0  # Thành công

