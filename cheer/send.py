"""시험기간(10/9~10/20) 매일 밤 23:15 KST에 성경 구절 응원 메일을 보낸다."""
import datetime as dt
import os
import smtplib
import sys
import time
from email.message import EmailMessage

TO = ["truthlumin@gmail.com", "truththeta@gmail.com", "has_26018@hana.hs.kr"]
KST = dt.timezone(dt.timedelta(hours=9))
SEND_AT = dt.time(23, 15)

# 날짜별 (구절, 출처, 응원 문장) — 하루도 겹치지 않게
MESSAGES = {
    "2026-10-09": (
        "내게 능력 주시는 자 안에서 내가 모든 것을 할 수 있느니라",
        "빌립보서 4:13",
        "시험기간 첫 밤이야. 오늘 공부한 만큼 내일의 네가 더 단단해져. 넌 할 수 있어!",
    ),
    "2026-10-10": (
        "강하고 담대하라 두려워하지 말며 놀라지 말라 네가 어디로 가든지 네 하나님 여호와가 너와 함께 하느니라",
        "여호수아 1:9",
        "시험이 두렵게 느껴져도 혼자가 아니야. 담대하게 한 걸음씩 가면 돼.",
    ),
    "2026-10-11": (
        "오직 여호와를 앙망하는 자는 새 힘을 얻으리니 독수리가 날개치며 올라감 같을 것이요 달음박질하여도 곤비하지 아니하겠고 걸어가도 피곤하지 아니하리로다",
        "이사야 40:31",
        "지칠 때쯤이지? 새 힘은 다시 채워져. 오늘은 푹 자고 내일 다시 날아오르자.",
    ),
    "2026-10-12": (
        "너는 마음을 다하여 여호와를 신뢰하고 네 명철을 의지하지 말라 너는 범사에 그를 인정하라 그리하면 네 길을 지도하시리라",
        "잠언 3:5-6",
        "결과는 맡기고 오늘 할 일에만 집중하자. 네 길은 이미 잘 인도받고 있어.",
    ),
    "2026-10-13": (
        "두려워하지 말라 내가 너와 함께 함이라 놀라지 말라 나는 네 하나님이 됨이라 내가 너를 굳세게 하리라 참으로 너를 도와 주리라",
        "이사야 41:10",
        "긴장되는 날에도 너를 붙드는 손이 있어. 오늘도 정말 수고 많았어.",
    ),
    "2026-10-14": (
        "너희를 향한 나의 생각을 내가 아나니 평안이요 재앙이 아니니라 너희에게 미래와 희망을 주는 것이니라",
        "예레미야 29:11",
        "지금의 노력은 분명 좋은 미래로 이어져. 희망을 놓지 마!",
    ),
    "2026-10-15": (
        "아무 것도 염려하지 말고 다만 모든 일에 기도와 간구로, 너희 구할 것을 감사함으로 하나님께 아뢰라",
        "빌립보서 4:6",
        "걱정은 내려놓고 감사로 오늘을 마무리하자. 시험 반환점, 여기까지 온 것도 대단해.",
    ),
    "2026-10-16": (
        "우리가 선을 행하되 낙심하지 말지니 포기하지 아니하면 때가 이르매 거두리라",
        "갈라디아서 6:9",
        "포기하지 않는 사람이 결국 거둬. 조금만 더 힘내자!",
    ),
    "2026-10-17": (
        "네 행사를 여호와께 맡기라 그리하면 네가 경영하는 것이 이루어지리라",
        "잠언 16:3",
        "준비한 것들을 맡기고 마음 편히 쉬어. 네가 계획한 대로 잘 될 거야.",
    ),
    "2026-10-18": (
        "하나님이 우리에게 주신 것은 두려워하는 마음이 아니요 오직 능력과 사랑과 절제하는 마음이니",
        "디모데후서 1:7",
        "넌 두려움이 아니라 능력을 받은 사람이야. 내일도 자신 있게!",
    ),
    "2026-10-19": (
        "너희 안에서 착한 일을 시작하신 이가 그리스도 예수의 날까지 이루실 줄을 우리는 확신하노라",
        "빌립보서 1:6",
        "시작한 걸 끝까지 해낼 수 있어. 마지막 스퍼트, 응원할게!",
    ),
    "2026-10-20": (
        "여호와께서 너를 지켜 모든 환난을 면하게 하시며 또 네 영혼을 지키시리로다 여호와께서 너의 출입을 지금부터 영원까지 지키시리로다",
        "시편 121:7-8",
        "시험기간 끝까지 정말 잘 해냈어! 결과와 상관없이 넌 최선을 다했고 그걸로 충분해. 고생 많았어 🎉",
    ),
}


def build(day: str) -> EmailMessage:
    verse, ref, cheer = MESSAGES[day]
    d = dt.date.fromisoformat(day)
    msg = EmailMessage()
    msg["Subject"] = f"[{d.month}/{d.day}] 오늘도 수고했어, 넌 잘 할 수 있어 💪"
    msg["From"] = os.environ["GMAIL_USER"]
    msg["To"] = ", ".join(TO)
    msg.set_content(f"“{verse}”\n— {ref}\n\n{cheer}\n")
    msg.add_alternative(
        f"""<div style="font-family:sans-serif;max-width:480px;line-height:1.7">
<p style="font-size:17px;padding:16px;border-left:4px solid #6b8afd;background:#f4f6ff">“{verse}”<br>
<span style="color:#666;font-size:14px">— {ref}</span></p>
<p style="font-size:16px">{cheer}</p></div>""",
        subtype="html",
    )
    return msg


def main() -> None:
    manual = os.environ.get("MANUAL") == "true"
    now = dt.datetime.now(KST)
    day = os.environ.get("FORCE_DATE") or now.date().isoformat()
    if day not in MESSAGES:
        print(f"{day}: 보낼 메시지 없음 (기간 외)")
        return
    if not manual:
        target = dt.datetime.combine(now.date(), SEND_AT, KST)
        wait = (target - now).total_seconds()
        if wait > 0:
            print(f"{int(wait)}초 기다렸다가 23:15 KST에 발송")
            time.sleep(wait)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.environ["GMAIL_USER"], os.environ["GMAIL_APP_PASSWORD"])
        s.send_message(build(day))
    print(f"{day} 메일 발송 완료 → {', '.join(TO)}")


if __name__ == "__main__":
    sys.exit(main())
