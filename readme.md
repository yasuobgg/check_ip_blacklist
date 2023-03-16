# Kiểm tra IP address của máy tính
- Sử dụng Python, VScode để viết, kiểm tra bằng Postman

1. Tìm nguồn IP độc hại (blacklist)
- Lấy danh sách những IP độc hại được gửi lên từ [các trang web hoặc blog](https://www.spamhaus.org/drop/drop.txt), có sẵn 
link trong file feeds.json
- truy cập {POST} http://127.0.0.1/isert_ip để gửi danh sách IP 
thu thập được lên MongoDB
- tiêu chí
* [x] Thu thập hết tất cả IP được liệt kê trong các URL của file feeds.json
* [x] Data thu thập không bị duplicate

2. Kiểm tra 1 IP bất kì được nhập từ bàn phím
- Kiểm tra xem IP đấy có đúng định dạng hay không, là IP Public hay Private
- Có trong blacklist (P1) của DB hay không
- truy cập {POST} http://127.0.0.1:5008/check_ip để kiểm tra
- đầu vào:
```
{
"ip":"1.19.0.0/16"
}
```
- đầu ra:
```
{
    "Is_public_or_private": "Public",
    "Is_valid_IP": "No",
    "Type": "blacklist",
    "Your_input_ip": "1.19.0.0/16"
}
```

3. Kiểm tra địa chỉ IP của máy tính của bạn
- IP được lấy ở [đây](https://branchup.pro/whatsmyip.php)
- Kiểm tra xem IP đấy có đúng định dạng hay không, là IP Public hay Private(mặc dù lấy ở trang trên luôn là public :D, => hơi ngu, sẽ sửa sau)
- Có trong blacklist (P1) của DB hay không
- Có thuộc [TOR node](https://check.torproject.org/exit-addresses) hay không
- truy cập {POST} http://127.0.0.1:5008/check_my_ip để kiểm tra 
- đầu vào:
    - Địa chỉ IP lấy được
- đầu ra:
```
{
    "Is_public_or_private": "Public",
    "Is_valid_IP": "Yes",
    "Type": "It's NOT a TOR exit node and NOT in blacklist",
    "Your_IP": "113.20.108.53"
}
```
4. Viết Dockerfile và docker-compose để tạo image và container
- tạo 1 network có tên là network-ver1 để cùng chạy 2 container, 1 là mongodb, 2 là file .py
- tạo docker container chạy image mongo, network là network-ver1
- database kết nối với mongodb localhost chạy trên dockercontainer, port 27017 có username,password đều là admin
- tạo image từ file .py, chạy container từ image vừa tạo
- Docker :
    -   docker pull mongo
    -   docker network create network-ver1
    -   docker run -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin -dp 27017:27017 --name mongo --network network-ver1 mongo
    -   docker build . -t datdo2509/ipcheckblacklist:ver1
    -   docker container run --name ipcheckblacklist -dp 5008:5008 --network network-ver1  datdo2509/ipcheckblacklist:ver1

* [x] Note: Khi chạy 2 container, chúng giao tiếp với nhau bằng DNS nội bộ, vì thế thuộc tính `host` phải đặt bằng tên miền, trong trường hợp
này là tên container chạy mongodb, chính là `mongo` ( --name), trong khi chạy riêng file .py ko trong container thì phải thay lại bằng `localhost`

enjoy! :D