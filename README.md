# Báo cáo bài tập lớn Python nhóm 3_13
# Thành viên nhóm
1. Phạm Tùng Dương - B20DCCN163
2. Đàm Trọng Ngọc Hà - B20DCCN211
3. Nguyễn Văn Đức - B20DCCN199
# Giới thiệu về game
- Tựa game đua xe mang tên "Horizon chase tunbo"
- Tựa game mang tính giải trí, là tựa game chiến thuật, tư duy để vượt qua các chướng ngại vật.
- Hình ảnh, âm thanh sống động khi chơi game và khi đụng chướng ngại vật. 
- Độ khó của game tăng dần theo thời gian
- Game có 2 chế độ
    + 1 người chơi
    + 2 người chơi
    
![image](https://user-images.githubusercontent.com/90205690/200451424-7de4b0d7-8482-4672-a9e3-c47351ef9d87.png)
# Thư viện sử dụng trong game
- Thread: xử lý đa luồng cho chức năng 2 người chơi
- Pygame: đóng vai trò chính, hỗ trợ tạo cửa sổ game, chạy game (vòng lặp), âm thanh, đồ họa, ...
# Quá trình làm việc
- Version 1.0: 
    + Xây dựng UI giao diện khi bắt đầu vào game
    + Xử lý thành công các nút chức năng cơ bản như là bắt đầu start game và các phím di chuyển
    + Xây dựng chức năng chọn xe cho người chơi
- Version 1.1:
    + Xây dựng đa luồng để xây dựng chức năng cho hai người chơi
    + Xây dựng chức năng chọn xe cho 2 người chơi
    + Xử lí một số lỗi click chuột
- Version 1.2: 
    + Xây dựng hàm xử lí âm thanh khi start game và âm thanh khi gặp chướng ngại vật
    + Hoàn thiện game và xử lí lỗi đa luồng khiến game bị lag
# Khó khăn còn gặp phải trong quá trình làm
- Sử dụng animation ở các nút chức năng (chưa làm được)
- Bất đồng bộ khi làm việc với thư viện Thread(đa luồng) và đã xử lý được bằng cách viết riêng hàm con với các biến khác nhau để luồng có thể hoạt động
# Mô tả các chức năng của game
-	Nút hướng dẫn chơi game
-	Nút tắt/bật âm thanh
-	Chọn số người chơi: 1 hoặc 2 người chơi.
-	Người chơi có thể chọn cho mình các loại xe đua khác nhau.
-	Khi gameover, người chơi có thể chơi lại bằng nút reload hoặc trở về giao diện chọn số người chơi bằng nút back.

# Hướng dẫn chạy game
1. Cài đặt môi trường python và ide Visual Studio code
2. Mở terminal và copy dòng lệnh "git clone https://github.com/PythonHDN/fa-3_13.git"
3. Mở thư mục ở trong Visual Studio Code hoặc các IDE khác
4. Run file racing.py
