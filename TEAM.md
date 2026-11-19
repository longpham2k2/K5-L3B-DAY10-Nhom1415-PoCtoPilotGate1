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

Trưởng nhóm · vai **Sản phẩm và kinh doanh**. Đề: câu 1.1, 1.5, 1.6 (Phiếu A mục A1, A3, A4, A5), câu 2.3 (Phiếu B mục B3), câu 2.9 (B7.4), quyết định v1 (B8); vòng 2: câu 3.0 (Phiếu C mục C0, C1), câu 3.4 (C6), câu 3.5 (C7, sửa phạm vi pilot); điều phối cả bàn, máy chạy chính cho mọi lần `eval` / `grade` / `check_submission`. File: `config/acceptance_criteria.json`, `config/operating_gates.json` mục `business`, `TEAM.md`.

### Đóng góp cụ thể

- Viết mục tiêu cấp hệ thống (1.1) dựa trên PRD v1.1 §2–§3 của Lab 9; viết Bản tiêu chí (1.6): 9 câu "Nếu … thì chúng tôi sẽ …", bốn câu soát, ranh giới đầu ra, ngày xem lại 2026-11-28.
- Điền và **ký** `config/acceptance_criteria.json` trước lần đánh giá đầu tiên (ký 16:01:57, lần `eval` đầu 16:13:14).
- Bản đồ dữ liệu và ví dụ drift REFUND-v3 → v4 (2026-12-01) ở B3.
- Đặt cổng kinh doanh (B7.4): trần hoàn ngày 1.000.000đ, ngân sách 1.500đ/ticket, phạm vi `all`, ROI 0,4; kiểm không regression.
- Quyết định v1 **Thu hẹp** (B8), dựa trên mốc base và prepared.
- Gom quy trình git của bàn (hợp nhất nhánh, xử lý xung đột) và nhận `runs/` về một máy chạy để nhật ký lần chạy liền mạch.
- **Vòng 2 (thẻ S4):** chạy mốc prepared (`grade --incident S4`) trước khi sửa; đối chiếu pre-mortem (C1).
- Phân tích nguyên nhân hàng chờ: 21 ca chuyển người đều đúng (15 hàng vỡ / thất lạc, 6 vượt ngân sách ngày sale), nên nút thắt là công suất người duyệt, không phải cổng chặn thừa.
- Thử hai phương án, mỗi lần đổi một thứ: thêm 1 người duyệt (hết ùn nhưng chi phí 7.157đ > trần đã ký 7.000đ → bỏ) và thu hẹp pilot về HN, HCM (0 ca ùn, chi phí 4.987đ, ROI 1,01 → chọn).
- Vẽ fault tree trước khi sửa (C6, ba nhánh ở ba tầng) và bảng sửa (C7: giảm hay ngăn từng nhánh).

### Bằng chứng

- Commit: `9c9fdec` (Sign acceptance criteria), `72e64c7`, `0979d00` (Phiếu A), `18dd45b` (B6, B8, C0, C1), `e555f23` (B7.4, cổng `business`), `8eb7259` (giữ byte bản chốt vòng 1 khớp `round1.lock`), `c4366ea` (vòng 2: thu hẹp pilot HN, HCM; C0, C6, C7), `d05a9e5` (C8 cập nhật số).
- Lần chạy: `R-base-prepared-20261119-162341-f7bb40` (bằng chứng v1), `R-base-after-20261119-170400-a63e67` và `R-S4-after-20261119-170410-a63e67` (sau khi điền `business`), `R-S4-grade-20261119-164200-22b003` (mốc prepared của thẻ S4), `R-S4-after-20261119-171703-0b04b2` (phương án 2 người, bị bỏ), `R-S4-after-20261119-171703-504920` (phương án HN, HCM), `R-base-after-20261119-171721-504920` (không regression), `R-S4-grade-20261119-171721-504920` (**PASS-VISIBLE**).
- Phiếu: A1, A3, A4, A5; B3, B6, B7.4, B8; C0, C1, C6, C7.

### Dùng AI

Dùng Claude (Claude Code) để đọc repo, soạn nháp câu trả lời trong phiếu, kiểm tra JSON tiêu chí trước khi ký, chạy lệnh đánh giá và soát chéo phần của các bạn. Mọi ngưỡng, con số và quyết định do bàn chốt.

### Exit ticket
- Tôi đã học được: Gate phòng ngừa cần được đặt ở ngoài model, và cần được tính lại từ các nguồn sự thật (có dẫn chứng, số liệu). Gate phòng ngừa cũng cần chặn được hết tác hại tiền và lỗi hãng của thẻ S4 (160.000đ -> 0.27 -> 0) mà không cần phải biết trước sự cố. Tuy nhiên, gate an toàn lại đẩy thêm việc sang phía người duyệt, nên an toàn và công suất phải được thiết kế cùng nhau.
- Tôi còn chưa nắm rõ: Thu hẹp phạm vi về chỉ HN và HCM dời được 18/41 ticket sang luồng làm thủ công, tôi không rõ liệu luồng đó có đủ nhân sự hay chỉ đẩy hàng chờ sang chỗ khác.

## TranTrongDat-2A202604030

### Phần việc phụ trách

Vai **Vận hành và pháp lý**. Đề: câu 1.2, 1.4 (Phiếu A mục A1, A2), câu 2.4 (Phiếu B mục B4 HAZOP vòng 1, B5 checklist 9 nhóm), câu 2.10 (B7.5 runbook 1–3, B7.6 giờ cao điểm); vòng 2: câu 3.7 (Phiếu C mục C9 fault tree sau khi sửa, C10 risk register, C11 checklist và runbook 4–5). File: `config/operating_gates.json` mục `operations`, `legal`.

### Đóng góp cụ thể

- Mục tiêu nhìn từ chị Oanh và chị Hạnh (1.2); telemetry production đo tỉ lệ lỗi hãng bị hãng phản ánh trong 7 ngày (1.4).
- HAZOP vòng 1 trên `issue_refund` (INVALID, INCOMPLETE, PERTURBED) và hai dòng ngoài kỹ thuật (người duyệt INCAPABLE, ngân sách WRONG); checklist 9 nhóm có PIC từng dòng.
- Cổng vận hành và pháp lý: PIC `NV-TUNG`, người duyệt `NV-HANH`, 6 ca/giờ, chờ tối đa 60 phút, 5 điều kiện dừng, kênh `#van-hanh-tro-ly`; chặn `recipient_contact`, `customer_note` gửi hãng; bắt buộc nguyên nhân khi ghi lỗi hãng.
- Runbook 1–3 (người chịu trách nhiệm, tín hiệu xanh/vàng/đỏ, dừng trong 5 phút do NV-TUNG bấm) và mục Giờ cao điểm theo dữ liệu thẻ S4.
- **Vòng 2 (thẻ S4):** cập nhật Runbook 1 và Giờ cao điểm khớp phạm vi mới (HN, HCM; DN, CT làm tay).
- Fault tree sau khi sửa (C9): nút `VÀ [gate … hỏng]` cho từng nhánh, ghi rõ nhánh nào ngăn, nhánh nào chỉ giảm, nhánh nào còn hở.
- Risk register (C10): tải HN, HCM tăng tiếp hoặc luồng làm tay DN, CT thiếu người; PIC NV-TUNG; dấu hiệu `queue_wait_max_min`, `queue_stuck`.
- Cập nhật checklist 9 nhóm với bằng chứng mới và PIC (C11); runbook 4 (sau sự cố) và runbook 5 (ba kịch bản tuần đầu).

### Bằng chứng

- Commit: `e6db255`, `a2ebead`, `82d115c` (1.2, 1.4), `04f96ee` (B4, B5), `5653d50`, `7abac16` (B7.5, B7.6, cổng `operations` / `legal`), `2225525` (C9, C10, C11; runbook khớp phạm vi HN, HCM).
- Lần chạy dẫn trong phiếu: `R-S4-grade-20261119-171721-504920`, `R-S4-after-20261119-171721-504920`, `R-base-after-20261119-171721-504920`.
- Phiếu: A1 câu 1.2, A2 cột telemetry; B4, B5, B7.5, B7.6; C9, C10, C11.

### Dùng AI
Tôi dùng ChatGPT/Codex để giải thích yêu cầu đề, đối chiếu PRD và repo, đề xuất hướng dẫn và kiểm tra lại nội dung cần thực hiện sao cho phù hợp hơn và đúng đắn hơn. Các phần nội dung đề xuất vẫn cần được kiểm tra và sửa lại để đồng bộ với các thông tin đang có.

### Exit ticket
Học được cách sử dụng HAZOP để đề xuất các bối cảnh tình huống xấu có thể xảy ra và lường trước mức độ hậu quả.  
Cần cân nhắc rủi ro từ nhiều bên khác nhau. Cần hỏi trước ai sẽ là người chịu hậu quả nếu agent đưa ra quyết định sai.  
Phân biệt giới hạn quyền tự động với giới hạn nghiệp vụ với tình huống trần tự động trong incident đề bài.  
  
Vướng mắc còn là vẫn chưa thực sự nắm rõ được khả năng, công suất thực sự làm việc của phần con người khi quy trình đẩy việc sang cho họ, giới hạn của con người về sức lực và chi phí có thể có sự khác biệt.


## NguyenCongHuy-2A202604086

### Phần việc phụ trách

Vai **Kỹ sư cổng: chạy và đánh giá**. Đề: câu 1.3 (Phiếu A mục A2), câu 2.1, 2.2 (Phiếu B mục B0, B1, B2), câu 2.6 (viết cổng vòng 1), câu 2.7, 2.8 (B7.2, B7.3), chốt cổng vòng 1; câu 3.1–3.3 (Phiếu C mục C2, C4, C5). File: `lab10/guards.py`.

### Đóng góp cụ thể

- Offline metric cho bước **chọn phê duyệt hợp lệ** (1.3), nhãn lấy từ `approvals` và sự kiện `approval_used`; không đo bước tìm kiếm phê duyệt.
- Viết cổng vòng 1 trong `lab10/guards.py` (đối chiếu nguồn sự thật, trần tiền và phê duyệt, lọc dữ liệu gửi bên thứ ba); chạy mốc base, after, prepared và chốt vòng 1.
- Lần chạy đầu và bảng soát lỗi `T-002@55` (hai lỗi chìm: hoàn sai 20.000đ, ghi oan VNX).
- Hai bước tránh rò rỉ dữ liệu; behavioral test với hai ticket hiểm (`O-1002`, `O-1019`).
- Phân tích thẻ S4: soát lỗi `S4-05@11`, `S4-08@11`, `S4-33@11`; HAZOP của thẻ; specification và giả định môi trường (LLM sẵn sàng giờ cao điểm).
- Đề xuất hai chỉ số theo dõi từ bảng soát lỗi thẻ: `fail_open_write_rate` (thành `fail_open_rate` của Khiêm) và `queue_over_sla_rate`.
- Đối chiếu chất lượng sau thay đổi: `R-S4-grade-20261119-171721-504920` đạt `PASS-VISIBLE`, hoàn sai/lỗi hãng oan 0/0; `R-base-after-20261119-171721-504920` không có regression trên bộ nền.

### Bằng chứng

- Commit: `06ad651`, `91caf76` (cổng và câu 1.3), `1753ce4` (chốt vòng 1, `round1.lock` lúc 16:23:40), `32739e8` (B0–B2), `e91229b` (B7.2, B7.3), `8df88c4` (C2, C4, C5).
- Lần chạy: `R-base-before-20261119-161314-f7bb40` (base), `R-base-after-20261119-162235-f7bb40`, `R-base-prepared-20261119-162341-f7bb40`; kiểm chứng thẻ S4: `R-S4-grade-20261119-171721-504920` và hồi quy `R-base-after-20261119-171721-504920`.
- Phiếu: A2 cột offline; B0, B1, B2, B7.2, B7.3; C2, C4, C5.

### Dùng AI

AI hỗ trợ đọc cấu trúc repo và trace, giải thích metric/cổng, soạn nháp các mục B0–B2, B7.2–B7.3, C2, C4, C5 và chạy các kiểm tra hành vi adhoc. Kết quả được đối chiếu với report và trace thực tế; nhóm tự chốt tiêu chí, cách diễn giải và quyết định.

### Exit ticket

Bài học: bộ nền chỉ nên là hồi quy, không phải toàn bộ bằng chứng để tối ưu; cần kiểm các bất biến trên dữ liệu holdout và ticket mới, không vá theo ID hay câu chữ. S4 cũng cho thấy pass về chất lượng chưa đủ để kết luận sẵn sàng vận hành: cần kiểm tải thật và năng lực người duyệt trước khi mở rộng.

## NguyenTrongKhiem-2A202604109

### Phần việc phụ trách

Vai **Kỹ sư cổng: lập trình**. Đề: câu 2.6 (Phiếu B mục B7.1), câu 3.5–3.6 (sửa code cổng vòng 2, chỉ số theo dõi mới trong `monitors.py`, đặc tả C8). File: `lab10/guards.py`, `lab10/monitors.py`.

### Đóng góp cụ thể

- Viết bảng 3 cổng phòng ngừa cấp hệ thống ở vòng 1 (B7.1): đối soát quyền lợi từ `orders.parcels` và `entitlement_vnd`, đối soát lỗi hãng qua `carrier_at_fault`, lọc sạch PII (`recipient_contact`, `customer_note`) khi gọi `notify_carrier`.
- Hiện thực hóa chỉ số telemetry production mới `fail_open_rate` trong `lab10/monitors.py`: bắt sự kiện `llm_fallback` mode `fail_open` khi nhà cung cấp LLM lỗi 429; giá trị 0,0 trên bộ nền, 0,185 trên gói S4 base và 0,24 trên mốc after (sáng đèn đúng kỳ vọng khi có sự cố).
- Viết toàn bộ đặc tả cho chỉ số mới ở Phiếu C mục C8: định nghĩa thước đo, nguồn dữ liệu từ trường `events`, công thức tính, cửa sổ trượt 60 phút / ca 480 phút, ngưỡng báo động `> 0.05` và điểm mù.
- Tối ưu `write_gate` vòng 2 trong `lab10/guards.py`: thêm nhánh từ chối ngay (`Verdict.deny`) với đơn giao đúng hạn (`delay == 0`), chặn dồn ca vào hàng chờ người duyệt không cần thiết khi model fallback.
- Đảm bảo toàn bộ 13/13 unit tests vượt qua, bộ nền đạt pass rate 1.0 (zero regression), `lab10.grade --incident S4` đạt **PASS-VISIBLE** với 5/5 hạng mục xanh (`integrity ✅`, `criteria ✅`, `visible ✅`, `regression ✅`, `monitor ✅`).

### Bằng chứng

- Commit: `fd6677f` (`monitors.py`, `guards.py`, B7.1), `1703c17` (C8).
- Lần chạy: `R-S4-grade-20261119-171138-618467` (`6 monitor ✅`, `5 regression ✅`), `R-S4-grade-20261119-172427-855fa8` (**PASS-VISIBLE**, sạch hoàn sai và lỗi oan hãng, 0 ca ùn, `fail_open_rate` 0,0 → 0,2435).
- Phiếu: B7.1; C8; đóng góp kỹ thuật cho C7.

### Dùng AI

Dùng Gemini (Antigravity) hỗ trợ rà soát logic điều kiện biên trong `write_gate` (xử lý ca `delay == 0`) và kiểm tra cấu trúc telemetry trong `monitors.py`. Mọi logic chặn, công thức tính và code sửa đổi đều được kiểm thử cục bộ bằng unit test và tự kiểm tra lệnh trước khi commit.

### Exit ticket

- **Một điều học được:** Gate an toàn phần mềm (code guard) phải nằm ngay trước lệnh ghi và đối soát trực tiếp từ nguồn sự thật (DB, chính sách) thay vì tin tưởng output của model; fallback an toàn không thể là "fail-open" tự tiện duyệt khi LLM mất kết nối, mà phải chặn hoặc phân luồng có kiểm soát.
- **Một điều còn chưa chắc:** Ngoài đời thực khi triển khai pilot quy mô lớn, nếu nhà cung cấp LLM nghẽn kéo dài nhiều giờ trong ngày siêu sale thì lượng ca chuyển người có làm vỡ năng lực chịu tải của đội ngũ vận hành hay không, cần dữ liệu đo lường thực tế từ pilot trước khi quyết định mở rộng ở Gate 2.
