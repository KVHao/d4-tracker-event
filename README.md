# Worldstone VN
Fan dashboard lấy cảm hứng từ Worldstone / r/Diablo4. Giờ hiển thị cố định Asia/Ho_Chi_Minh (UTC+7).

## Deploy GitHub Pages
1. Upload toàn bộ thư mục này vào repository.
2. Settings → Pages → Deploy from a branch → `main` / root.
3. Actions phải được bật. Workflow `Update Sanctuary data` chạy 5 phút/lần để cập nhật event và 15 phút/lần cho feed (workflow chung chạy 5 phút; script tự refresh cả hai).

## Dữ liệu
- World Boss: đọc trang công khai Helltides.com/worldboss rồi ghi vào `data/events.json`.
- Helltide/Realmwalker/Legion: countdown client-side theo chu kỳ công khai; có thể thay bằng endpoint chính xác nếu Helltides/Demonly cung cấp API công khai.
- Tracker: script cố đọc BlizzTrack + Blizzard News, giữ lại `data/news.json` cũ nếu nguồn lỗi.

Ảnh banner World Boss trong `assets/world-boss.webp` được crop từ ảnh Worldstone mà chủ repo cung cấp. Nếu muốn dùng asset gốc trực tiếp, hãy thay file này bằng asset bạn có quyền sử dụng.

Lưu ý: GitHub Actions cron không bảo đảm chạy đúng từng phút tuyệt đối. Browser notification hoạt động khi trang đang mở; push khi trang đóng cần Web Push backend/service worker.
