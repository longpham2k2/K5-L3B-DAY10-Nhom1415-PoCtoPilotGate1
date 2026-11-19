"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    ticket = ctx.ticket
    order_id = ticket.get("order_id")
    order = ctx.tools.lookup_order(order_id) if order_id else None
    if order is None:
        ctx.log("unknown_order", order_id=order_id)
        return Verdict.escalate("không tìm thấy đơn trong dữ liệu nguồn")
    if order.get("customer_id") != ticket.get("customer_id"):
        ctx.log("order_owner_mismatch", order_id=order_id)
        return Verdict.escalate("người gửi không phải chủ đơn")

    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        ctx.log("missing_effective_policy", as_of=ctx.as_of)
        return Verdict.escalate("không tìm thấy chính sách có hiệu lực")

    ctx.log("policy_pinned", policy_id=policy["policy_id"])
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order is None or order.get("customer_id") != ctx.ticket.get("customer_id"):
            ctx.log("refund_order_mismatch", order_id=action.get("order_id"))
            return Verdict.escalate("không xác minh được chủ đơn")

        if order.get("refund_status") == "REFUNDED":
            ctx.log("refund_already_completed", order_id=order["order_id"])
            return Verdict.deny("đơn đã được hoàn tiền")
        if ctx.tools.ledger_rows(ticket_id=action.get("ticket_id"), order_id=order["order_id"]):
            ctx.log("duplicate_refund", order_id=order["order_id"])
            return Verdict.deny("ticket này đã có giao dịch hoàn tiền")

        policies = ctx.tools.lookup_policies()
        policy = H.effective_policy(policies, ctx.as_of)
        if policy is None:
            ctx.log("missing_effective_policy", as_of=ctx.as_of)
            return Verdict.escalate("không tìm thấy chính sách có hiệu lực")
        try:
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        except (KeyError, ValueError):
            ctx.log("missing_tracking_facts", order_id=order["order_id"])
            return Verdict.escalate("không đủ dữ liệu theo dõi để xác minh hoàn tiền")
        delay = H.db_delay_days(parcel, ctx.as_of)
        cause = parcel.get("delay_cause")
        if cause is None:
            ctx.log("unknown_delay_cause", parcel_id=parcel["parcel_id"])
            return Verdict.escalate("chưa xác định được nguyên nhân giao trễ")

        entitlement = H.entitlement_vnd(policy, order, delay, cause)
        amount = action.get("amount_vnd")
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            ctx.log("invalid_refund_amount", amount_vnd=amount)
            return Verdict.deny("số tiền hoàn không hợp lệ")
        if amount > entitlement:
            ctx.log("refund_exceeds_entitlement", requested=amount, entitled=entitlement,
                    delay_days=delay, policy_id=policy["policy_id"])
            return Verdict.deny("số tiền yêu cầu vượt quyền lợi theo chính sách và dữ liệu giao hàng")
        if action.get("payer", "LOGIX") != "LOGIX":
            ctx.log("invalid_refund_payer", payer=action.get("payer"))
            return Verdict.deny("người chi trả không được chính sách cho phép")

        approval_id = action.get("approval_id")
        if approval_id:
            approvals = ctx.tools.lookup_approvals(approval_id=approval_id)
            approval = approvals[0] if approvals else None
            expected_approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
            valid = (
                approval is not None
                and approval.get("status") == "valid"
                and approval.get("order_id") == order["order_id"]
                and approval.get("customer_id") == ctx.ticket.get("customer_id")
                and approval.get("max_vnd", 0) >= amount
                and H.d(ctx.as_of) <= H.d(approval["expires_at"])
                and (approval.get("ticket_id") in (None, action.get("ticket_id")))
                and (not expected_approver or approval.get("approver_id") == expected_approver)
            )
            if not valid:
                ctx.log("invalid_refund_approval", approval_id=approval_id, order_id=order["order_id"])
                return Verdict.escalate("phê duyệt không hợp lệ hoặc không khớp giao dịch")
        elif amount > policy["auto_limit_vnd"]:
            ctx.log("approval_required", amount_vnd=amount, limit_vnd=policy["auto_limit_vnd"])
            return Verdict.escalate("khoản hoàn vượt hạn mức tự động, cần người duyệt")

        paid = order["goods_value_vnd"] + order["shipping_fee_vnd"]
        already_paid = sum(row["amount_vnd"] for row in ctx.tools.ledger_rows(order_id=order["order_id"]))
        if already_paid + amount > paid:
            ctx.log("refund_exceeds_order_value", order_id=order["order_id"])
            return Verdict.deny("tổng tiền hoàn vượt giá trị đơn")

        if not approval_id:
            limits = ctx.tools.ops_limits()
            today_auto = ctx.tools.auto_refund_today_vnd()
            customer_auto = sum(
                event.get("amount_vnd", 0)
                for event in ctx.events
                if event.get("type") == "tool"
                and event.get("tool") == "issue_refund"
                and event.get("customer_id") == ctx.ticket.get("customer_id")
                and not event.get("approval_id")
            )
            cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")
            if cap is not None and today_auto + amount > cap:
                ctx.log("daily_refund_cap", cap=cap, today=today_auto, asked=amount)
                return Verdict.escalate("vượt trần tiền hoàn tự động mỗi ngày")
            customer_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
            if customer_cap is not None and customer_auto + amount > customer_cap:
                ctx.log("customer_refund_cap", cap=customer_cap, today=customer_auto, asked=amount)
                return Verdict.escalate("vượt trần hoàn tự động cho khách trong ngày")
            daily_budget = limits.get("daily_auto_refund_budget_vnd")
            if daily_budget is not None and today_auto + amount > daily_budget:
                ctx.log("daily_auto_refund_budget", cap=daily_budget, today=today_auto, asked=amount)
                return Verdict.escalate("vượt ngân sách hoàn tự động trong ngày")

    elif tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order is None or order.get("customer_id") != ctx.ticket.get("customer_id"):
            ctx.log("fault_order_mismatch", order_id=action.get("order_id"))
            return Verdict.deny("không xác minh được đơn để ghi lỗi hãng")
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        if policy is None:
            ctx.log("missing_effective_policy", as_of=ctx.as_of)
            return Verdict.escalate("không tìm thấy chính sách có hiệu lực")
        try:
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        except (KeyError, ValueError):
            ctx.log("missing_tracking_facts", order_id=order["order_id"])
            return Verdict.deny("không đủ dữ liệu theo dõi để ghi lỗi hãng")
        delay = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(policy, parcel, delay):
            ctx.log("carrier_fault_not_supported", parcel_id=parcel["parcel_id"], delay_days=delay,
                    cause=parcel.get("delay_cause"))
            return Verdict.deny("dữ liệu và chính sách không xác nhận lỗi của hãng")
        if action.get("parcel_id") != parcel["parcel_id"] or action.get("carrier_id") != parcel["carrier_id"]:
            ctx.log("carrier_fault_corrected", parcel_id=parcel["parcel_id"])
            return Verdict.modify("dùng kiện và hãng theo dữ liệu theo dõi",
                                  parcel_id=parcel["parcel_id"], carrier_id=parcel["carrier_id"],
                                  driver_id=parcel.get("driver_id"), delay_days=delay)
        if action.get("delay_days") != delay:
            ctx.log("carrier_fault_delay_corrected", parcel_id=parcel["parcel_id"], delay_days=delay)
            return Verdict.modify("dùng số ngày trễ theo dữ liệu theo dõi", delay_days=delay)

        limits = ctx.tools.ops_limits()
        strike_limit = limits.get("max_auto_strikes_per_carrier_per_day")
        strikes = len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"]))
        if strike_limit is not None and strikes >= strike_limit:
            ctx.log("carrier_strike_limit", carrier_id=parcel["carrier_id"], strikes=strikes,
                    limit=strike_limit)
            return Verdict.escalate("đạt trần ghi lỗi tự động cho hãng trong ngày")

    elif tool == "notify_carrier":
        policies = ctx.tools.lookup_policies()
        policy = H.effective_policy(policies, ctx.as_of)
        if policy is None:
            ctx.log("missing_effective_policy", as_of=ctx.as_of)
            return Verdict.escalate("không tìm thấy chính sách có hiệu lực")
        payload = action.get("payload")
        if not isinstance(payload, dict):
            ctx.log("invalid_carrier_payload")
            return Verdict.deny("nội dung gửi hãng không hợp lệ")
        order_id, parcel_id = payload.get("order_id"), payload.get("parcel_id")
        recorded = ctx.tools.fault_rows(ticket_id=action.get("ticket_id"), order_id=order_id,
                                        parcel_id=parcel_id, carrier_id=action.get("carrier_id"))
        if not recorded:
            ctx.log("carrier_notice_without_recorded_fault", order_id=order_id, parcel_id=parcel_id)
            return Verdict.deny("chưa có lỗi hãng đã được xác minh")
        allowed = set(policy.get("carrier_notice_fields", []))
        blocked = set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
        safe_payload = {key: value for key, value in payload.items() if key in allowed and key not in blocked}
        if safe_payload != payload:
            dropped = sorted(set(payload) - set(safe_payload))
            ctx.log("carrier_payload_filtered", dropped=dropped)
            return Verdict.modify("chỉ gửi trường được chính sách cho phép", payload=safe_payload)

    elif tool == "send_reply":
        if action.get("customer_id") != ctx.ticket.get("customer_id"):
            ctx.log("reply_customer_mismatch", customer_id=action.get("customer_id"))
            return Verdict.deny("người nhận không khớp khách hàng của ticket")
        if action.get("amount_vnd", 0) > 0:
            rows = ctx.tools.ledger_rows(ticket_id=action.get("ticket_id"),
                                         order_id=ctx.ticket.get("order_id"))
            if not any(row["amount_vnd"] == action["amount_vnd"] for row in rows):
                ctx.log("reply_claims_unrecorded_refund", amount_vnd=action["amount_vnd"])
                return Verdict.deny("không thể báo đã hoàn khi sổ cái chưa ghi nhận")

    else:
        ctx.log("unknown_write_tool", tool=tool)
        return Verdict.deny("công cụ ghi không được cho phép")

    return Verdict.allow()
