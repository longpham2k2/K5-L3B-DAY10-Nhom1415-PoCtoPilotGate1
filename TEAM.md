# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Nhom1415
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-Nhom1415-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S4

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Phạm Ngọc Long | 2A202604111 | Sản phẩm và kinh doanh | x |
|   2 | Trần Trọng Đạt | 2A202604030 | Vận hành và pháp lý | |
|   3 | Nguyễn Công Huy | 2A202604086 | Kỹ sư cổng: Chạy & đánh giá | |
|   4 | Nguyễn Trọng Khiêm | 2A202604109 | Kỹ sư cổng: Lập trình | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## PhamNgocLong-2A202604111

### Phần việc phụ trách

Trưởng nhóm · vai **Sản phẩm và kinh doanh**. Đề: câu 1.1, 1.5, 1.6 (Phiếu A mục A1, A3, A4, A5), câu 2.3 (Phiếu B mục B3), câu 2.9 (B7.4), quyết định v1 (B8); điều phối cả bàn, máy chạy chính cho mọi lần `eval` / `grade` / `check_submission`. File: `config/acceptance_criteria.json`, `config/operating_gates.json` mục `business`, `TEAM.md`.

### Đóng góp cụ thể

- Viết mục tiêu cấp hệ thống (1.1) dựa trên PRD v1.1 §2–§3 của Lab 9; viết Bản tiêu chí (1.6): 9 câu "Nếu … thì chúng tôi sẽ …", bốn câu soát, ranh giới đầu ra, ngày xem lại 2026-11-28.
- Điền và **ký** `config/acceptance_criteria.json` trước lần đánh giá đầu tiên (ký 16:01:57, lần `eval` đầu 16:13:14).
- Bản đồ dữ liệu và ví dụ drift REFUND-v3 → v4 (2026-12-01) ở B3.
- Đặt cổng kinh doanh (B7.4): trần hoàn ngày 1.000.000đ, ngân sách 1.500đ/ticket, phạm vi `all`, ROI 0,4; kiểm không regression.
- Quyết định v1 **Thu hẹp** (B8), dựa trên mốc base và prepared.
- Gom quy trình git của bàn (hợp nhất nhánh, xử lý xung đột) và nhận `runs/` về một máy chạy để nhật ký lần chạy liền mạch.

### Bằng chứng

- Commit: `9c9fdec` (Sign acceptance criteria), `72e64c7`, `0979d00` (Phiếu A), `18dd45b` (B6, B8, C0, C1), `e555f23` (B7.4, cổng `business`), `8eb7259` (giữ byte bản chốt vòng 1 khớp `round1.lock`).
- Lần chạy: `R-base-prepared-20261119-162341-f7bb40` (bằng chứng v1), `R-base-after-20261119-170400-a63e67` và `R-S4-after-20261119-170410-a63e67` (sau khi điền `business`), `R-S4-grade-20261119-164200-22b003` (mốc prepared của thẻ S4).
- Phiếu: A1, A3, A4, A5; B3, B7.4, B8.

### Dùng AI

Dùng Claude (Claude Code) để đọc repo, soạn nháp câu trả lời trong phiếu, kiểm tra JSON tiêu chí trước khi ký, chạy lệnh đánh giá và soát chéo phần của các bạn. Mọi ngưỡng, con số và quyết định do bàn chốt.

### Exit ticket
...

## TranTrongDat-2A202604030

### Phần việc phụ trách

Vai **Vận hành và pháp lý**. Đề: câu 1.2, 1.4 (Phiếu A mục A1, A2), câu 2.4 (Phiếu B mục B4 HAZOP vòng 1, B5 checklist 9 nhóm), câu 2.10 (B7.5 runbook 1–3, B7.6 giờ cao điểm). File: `config/operating_gates.json` mục `operations`, `legal`.

### Đóng góp cụ thể

- Mục tiêu nhìn từ chị Oanh và chị Hạnh (1.2); telemetry production đo tỉ lệ lỗi hãng bị hãng phản ánh trong 7 ngày (1.4).
- HAZOP vòng 1 trên `issue_refund` (INVALID, INCOMPLETE, PERTURBED) và hai dòng ngoài kỹ thuật (người duyệt INCAPABLE, ngân sách WRONG); checklist 9 nhóm có PIC từng dòng.
- Cổng vận hành và pháp lý: PIC `NV-TUNG`, người duyệt `NV-HANH`, 6 ca/giờ, chờ tối đa 60 phút, 5 điều kiện dừng, kênh `#van-hanh-tro-ly`; chặn `recipient_contact`, `customer_note` gửi hãng; bắt buộc nguyên nhân khi ghi lỗi hãng.
- Runbook 1–3 (người chịu trách nhiệm, tín hiệu xanh/vàng/đỏ, dừng trong 5 phút do NV-TUNG bấm) và mục Giờ cao điểm theo dữ liệu thẻ S4.

### Bằng chứng

- Commit: `e6db255`, `a2ebead`, `82d115c` (1.2, 1.4), `04f96ee` (B4, B5), `5653d50`, `7abac16` (B7.5, B7.6, cổng `operations` / `legal`).
- Phiếu: A1 câu 1.2, A2 cột telemetry; B4, B5, B7.5, B7.6.

### Dùng AI
...

### Exit ticket
...

## NguyenCongHuy-2A202604086

### Phần việc phụ trách

Vai **Kỹ sư cổng: chạy và đánh giá**. Đề: câu 1.3 (Phiếu A mục A2), câu 2.1, 2.2 (Phiếu B mục B0, B1, B2), câu 2.6 (viết cổng vòng 1), câu 2.7, 2.8 (B7.2, B7.3), chốt cổng vòng 1; câu 3.1–3.3 (Phiếu C mục C2, C4, C5). File: `lab10/guards.py`.

### Đóng góp cụ thể

- Offline metric cho bước "tìm phê duyệt" (1.3), nhãn lấy từ `approvals`.
- Viết cổng vòng 1 trong `lab10/guards.py` (đối chiếu nguồn sự thật, trần tiền và phê duyệt, lọc dữ liệu gửi bên thứ ba); chạy mốc base, after, prepared và chốt vòng 1.
- Lần chạy đầu và bảng soát lỗi `T-002@55` (hai lỗi chìm: hoàn sai 20.000đ, ghi oan VNX).
- Hai bước tránh rò rỉ dữ liệu; behavioral test với hai ticket hiểm (`O-1002`, `O-1019`).
- Phân tích thẻ S4: soát lỗi `S4-05@11`, `S4-08@11`, `S4-33@11`; HAZOP của thẻ; specification và giả định môi trường (LLM sẵn sàng giờ cao điểm).

### Bằng chứng

- Commit: `06ad651`, `91caf76` (cổng và câu 1.3), `1753ce4` (chốt vòng 1, `round1.lock` lúc 16:23:40), `32739e8` (B0–B2), `e91229b` (B7.2, B7.3), `8df88c4` (C2, C4, C5).
- Lần chạy: `R-base-before-20261119-161314-f7bb40` (base), `R-base-after-20261119-162235-f7bb40`, `R-base-prepared-20261119-162341-f7bb40`.
- Phiếu: A2 cột offline; B0, B1, B2, B7.2, B7.3; C2, C4, C5.

### Dùng AI
...

### Exit ticket
...

## NguyenTrongKhiem-2A202604109

### Phần việc phụ trách

Vai **Kỹ sư cổng: lập trình**. Đề: câu 2.6 (Phiếu B mục B7.1), câu 3.5–3.6 (sửa cổng vòng 2, chỉ số theo dõi mới). File: `lab10/guards.py`, `lab10/monitors.py`.

### Đóng góp cụ thể

- Bảng cổng phòng ngừa vòng 1 (B7.1).
- Chỉ số theo dõi mới `fail_open_rate` trong `lab10/monitors.py`: tỉ lệ trial mà trợ lý rơi về `llm_fallback` chế độ `fail_open`; bằng 0,0 trên bộ nền và 0,185 trên gói S4 (sáng đèn khi sự cố xảy ra).
- Nhánh vòng 2 trong `write_gate` khi `issue_refund`: đơn giao đúng hạn (`delay == 0`) thì từ chối thay vì chuyển người.

### Bằng chứng

- Commit: `fd6677f` (`monitors.py`, `guards.py`, B7.1).
- Lần chạy: `R-S4-grade-20261119-171138-618467` (`6 monitor ✅`, `5 regression ✅`).
- Phiếu: B7.1.

### Dùng AI
...

### Exit ticket
...
