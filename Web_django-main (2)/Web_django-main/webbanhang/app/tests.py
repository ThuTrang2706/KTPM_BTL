import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import Product, Order, OrderItem

#Dang ky
@pytest.mark.django_db
def test_register(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'password1': 'testpassword123',
        'password2': 'testpassword123'
    })
    assert response.status_code == 302  # Redirect after successful registration
    assert User.objects.filter(username='testuser').exists()
    
# Test mật khẩu không khớp
@pytest.mark.django_db
def test_register_password_mismatch(client):
    response = client.post(reverse('register'), {
        'username': 'user1',
        'password1': 'password123',
        'password2': 'password1234'
    })
    assert response.status_code == 200 
    assert b"Passwords do not match." in response.content  
    

# Test thiếu thông tin (Tên người dùng trống)
@pytest.mark.django_db
def test_register_missing_field(client):
    response = client.post(reverse('register'), {
        'username': '',  # Thiếu tên người dùng
        'password1': 'password123',
        'password2': 'password123'
    })
    assert response.status_code == 200  
    assert b"Username and password cannot be empty!" in response.content  
    
# Test thiếu thông tin (Mật khẩu trống)
@pytest.mark.django_db
def test_register_missing_field(client):
    response = client.post(reverse('register'), {
        'username': 'username',
        'password1': '',  # Thiếu mật khẩu
        'password2': 'password123'
    })
    assert response.status_code == 200  
    assert b"Username and password cannot be empty!" in response.content  

# Test tên người dùng đã tồn tại
@pytest.mark.django_db
def test_register_username_exists(client):
    # Tạo một người dùng ban đầu
    User.objects.create_user(username='existinguser', password='password123')

    response = client.post(reverse('register'), {
        'username': 'existinguser',  # Username đã tồn tại
        'password1': 'newpassword123',
        'password2': 'newpassword123'
    })
    assert response.status_code == 200  
    assert b"Username already exists!" in response.content  # Kiểm tra thông báo lỗi
    
@pytest.mark.django_db
def test_register_invalid_username(client):
    User.objects.create_user(username='validuser', password='password123')
    response = client.post(reverse('register'), {
        'username': 'invalid user',  # Tên người dùng không hợp lệ (có khoảng trắng)
        'password1': 'password123',
        'password2': 'password123'
    })
    assert response.status_code == 200  
    assert b"Username cannot contain spaces or special characters (except underscore)." in response.content  # Kiểm tra thông báo lỗi
    
@pytest.mark.django_db
def test_register_invalid_password(client):
    response = client.post(reverse('register'), {
        'username': 'validuser',
        'password1': 'invalid password',  # Mật khẩu không hợp lệ (có khoảng trắng)
        'password2': 'invalid password'
    })
    assert response.status_code == 200
    assert b"Password contains invalid characters" in response.content  # Kiểm tra thông báo lỗi
    
@pytest.mark.django_db
def test_register_short_password(client):
    response = client.post(reverse('register'), {
        'username': 'validuser',
        'password1': 'short',  # Mật khẩu quá ngắn
        'password2': 'short'
    })
    assert response.status_code == 200
    assert b"Password must be at least 8 characters long." in response.content
    

##############################################################################################################################################
#Dang nhap
@pytest.mark.django_db
def test_login(client):
    #Đăng nhập thành công
    user = User.objects.create_user(username='testuser', password='testpassword123')
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'testpassword123'
    })
    assert response.status_code == 302  # Redirect to home after login
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_login_wrong_password(client):
    #Đăng nhập thất bại do sai mật khẩu
    User.objects.create_user(username='testuser', password='testpassword123')
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200  # Không redirect, vẫn ở trang login
    assert b"user or password not correct!" in response.content

@pytest.mark.django_db
def test_login_non_existent_user(client):
    #Đăng nhập thất bại do username không tồn tại
    response = client.post(reverse('login'), {
        'username': 'wronguser',
        'password': 'testpassword123'
    })
    assert response.status_code == 200
    assert b"user or password not correct!" in response.content


@pytest.mark.django_db
def test_login_empty_fields(client):
    #Đăng nhập thất bại khi không nhập thông tin
    response = client.post(reverse('login'), {
        'username': ' ',
        'password': ''
    })
    assert response.status_code == 200
    assert b"username or password not empty!" in response.content


@pytest.mark.django_db
def test_login_only_username(client):
    #Đăng nhập thất bại khi chỉ nhập username
    User.objects.create_user(username='testuser', password='testpassword123')
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': ''
    })
    assert response.status_code == 200
    assert b"username or password not empty!" in response.content


@pytest.mark.django_db
def test_login_only_password(client):
    #Đăng nhập thất bại khi chỉ nhập password
    User.objects.create_user(username='testuser', password='testpassword123')
    response = client.post(reverse('login'), {
        'username': '',
        'password': 'testpassword123'
    })
    assert response.status_code == 200
    assert b"username or password not empty!" in response.content

##############################################################################################################################################
#Cap nhat gio hang
@pytest.mark.django_db
def test_update_cart(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    product = Product.objects.create(name='Test Product', price=10.0)
    response = client.post(reverse('update_item'), data={
        'productId': product.id,
        'action': 'add'
    }, content_type='application/json')
    
    assert response.status_code == 200
    order = Order.objects.get(customer=user, complete=False)
    order_item = OrderItem.objects.get(order=order, product=product)
    assert order_item.quantity == 1
    

@pytest.mark.django_db
def test_increment_existing_product_quantity(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    product = Product.objects.create(name='Test Product', price=10.0)
    order = Order.objects.create(customer=user, complete=False)
    OrderItem.objects.create(order=order, product=product, quantity=2)

    response = client.post(reverse('update_item'), data={
        'productId': product.id,
        'action': 'add'
    }, content_type='application/json')

    order_item = OrderItem.objects.get(order=order, product=product)
    assert order_item.quantity == 3

@pytest.mark.django_db
def test_decrement_product_quantity(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    product = Product.objects.create(name='Test Product', price=10.0)
    order = Order.objects.create(customer=user, complete=False)
    OrderItem.objects.create(order=order, product=product, quantity=2)

    response = client.post(reverse('update_item'), data={
        'productId': product.id,
        'action': 'remove'
    }, content_type='application/json')

    order_item = OrderItem.objects.get(order=order, product=product)
    assert order_item.quantity == 1

@pytest.mark.django_db
def test_remove_product_from_cart_when_quantity_zero(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    product = Product.objects.create(name='Test Product', price=10.0)
    order = Order.objects.create(customer=user, complete=False)
    order_item = OrderItem.objects.create(order=order, product=product, quantity=1)

    response = client.post(reverse('update_item'), data={
        'productId': product.id,
        'action': 'remove'
    }, content_type='application/json')
    assert response.status_code == 200
    assert OrderItem.objects.filter(order=order, product=product).exists() is False
    with pytest.raises(OrderItem.DoesNotExist):
        OrderItem.objects.get(pk=order_item.pk)

@pytest.mark.django_db
def test_unauthenticated_user_cannot_update_cart(client):
    product = Product.objects.create(name='Test Product', price=10.0)
    
    response = client.post(reverse('update_item'), data={
        'productId': product.id,
        'action': 'add'
    }, content_type='application/json')
    
    assert response.status_code == 302