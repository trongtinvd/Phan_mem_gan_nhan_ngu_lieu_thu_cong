# Phan_mem_gan_nhan_ngu_lieu_thu_cong

#Tính năng tách câu thủ công
-Tính năng này cho phép người tách câu thủ công bằng cách tự phát hiện vị trí cuối câu và nhấn xuống dòng tại vị trí đó
-Ngoài ra ứng dụng tính năng tách câu bằng regex, người dùng tự nhập các patern vào 2 ô search và replace để thay các vị trí cuối công bằng ký tự xuống dòng
-Về cơ bản thì việc tách câu trên ứng dụng này không khác gì trên các phần mềm như notepad

#Tính năng tách từ và dán nhãn từ loại
-Người dùng có thể bắt đầu sử dụng tính năng này bằng cách chọn một file text để tải lên hoặc copy & paste đoạn văn bản trực tiếp vào textbox
-Sau khi đã có đoạn văn bản, người dùng sẽ cần phải dùng chuột để bôi đen từng từ trong textbox
	+ứng dụng sẽ bắt lại từ đó và cho vào một hộp thoại bên cạnh textbox, kế bên nó là một drop-down list để người dùng chọn loại từ tương ứng
	+sau khi đã chọn xong người dùng có thể nhân nút “lưu” để lưu từ đó vào memory database của ứng dụng
	+tất cả những từ trong database này sẽ được hiễn thị theo danh sách bên cạch textbox, đòng thời ứng dụng sẽ kiểm tra và hightlight các từ tương tự trong textbox để đánh dấu cho người dùng biết là từ đó đã có trong memory database
-Phần mềm cũng hỗ trợ việc xóa và chỉnh sửa những từ đã có trong memory database bằng cách nhấp chọn từ mình muốn trên bảng rồi nhấn chọn một trong 2 nút “xóa”, “sủa” bên dưới
	+Đối với tính năng chỉnh sủa từ thì một hộp thoại mới sẽ hiện ra gồm từ đã chọn và loại từ của nó đã lưu, người dùng có thể chỉnh sửa nội dụng 2 thành phần này rồi nhấn nút "lưu" để lưu thay đổi
	+Đối với tính năng xóa từ thì xin xác nhận của người dùng trước khi xóa từ đó
	
#Tính năng dán nhãn thực thể
-Tương tự như phần dán nhãn từ loại nhưng dùng để dán nhãn thực thể 

#Quản lý database
-Dây là nơi người dùng quản lý database chính của phần mềm
-Những dữ liệu người dùng thêm vào trong 2 tính năng trên sẽ chỉ được lưu trên memory database và sẽ mất đi khi người dùng đóng phần mềm
-Để lưu những thay đổi từ memory database xuống database chính thì người dùng phải nhấn nút "lưu DB"
-Tại đây người dùng cũng có thể chỉnh sửa dữ liệu trong database bằng cách chọn các cặp từ loại hạy thực thể trong 2 bảng bên và thực hiện xóa hay sửa các dữ liệu này 