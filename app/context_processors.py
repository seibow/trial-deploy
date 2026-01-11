from django.utils import timezone
import random

def season_image(request):
    current_month = timezone.localtime().month
    return {"season_image": f"img/season/{current_month:02d}.png"}

def random_message(request):
    """
    全テンプレートで使えるランダムメッセージを返す。
    リクエストごと（ページ読み込みごと）に選ばれます。
    """
    messages = [
        "お疲れさまです🌙",
        "コツコツ進めましょう🐰",
        "頑張っててえらいよ✨",
        "できることから、ひとつずつ。"
    ]
    message = random.choice(messages)
    return {"message": message}
