from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, date
from .models import GoalsModel
from app.steps.models import StepsModel
from collections import defaultdict
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import math


User = get_user_model()

@login_required
@require_http_methods(["GET", "POST"])
def goals_index(request, user_id=None):
    # /goals/   → 自分の一覧
    # /goals/1/ → 指定ユーザーの一覧
    target_user = request.user if user_id is None else get_object_or_404(User, pk=user_id)
    birthday = target_user.birthday
    # ここで target_user のゴールを取得してテンプレへ
    goals = GoalsModel.objects.filter(user=target_user).order_by("limit_age")
    # future_age ごとにグループ化し、件数も同時に集計
    goals_by_age = defaultdict(lambda: {"goals": [], "total": 0, "done_count": 0})
    ctx = {"profile_user": target_user}
    for goal in goals:
        limit_age = goal.limit_age
        future_age = limit_age.year - birthday.year - ((limit_age.month, limit_age.day) < (birthday.month, birthday.day))
        future_month = f"{limit_age.month}月"

        goals_by_age[future_age]["goals"].append({
            "id": goal.id,
            "title": goal.title,
            "limit_age": goal.limit_age,
            "future_age": future_age,
            "future_month": future_month,
            "is_done": goal.is_done,
        })
        # 同年齢の全目標数をカウント
        goals_by_age[future_age]["total"] += 1
        # その中で達成済の数をカウント
        if goal.is_done:
            goals_by_age[future_age]["done_count"] += 1
    
    for future_age, data in goals_by_age.items():
        done = data.get("done_count", 0)
        total = data.get("total", 0)

        # 0/x はすべて 0-0.png にする
        if done == 0 and total > 0:
            image_file = "0-0.png"

        # 0/0 も 0-0.png
        elif total == 0:
            image_file = "0-0.png"

        else:
            # done > 0 かつ total > 0 のときだけ約分する
            g = math.gcd(done, total)
            reduced_done = done // g
            reduced_total = total // g

            image_file = f"{reduced_done}-{reduced_total}.png"

        data["moon_image"] = image_file

    sorted_ages = sorted(goals_by_age.keys())  # 年齢順
    active_age = request.GET.get("active_age")
    if active_age is None:
        # 初期表示は最も若い age
        active_age = sorted_ages[0] if sorted_ages else None
    else:
        # GET パラメータがあれば文字列なので int に変換
        active_age = int(active_age)

    # 年齢順に並び替え
    sorted_goals_by_age = dict(sorted(goals_by_age.items()))

    return render(request, "goals/home.html", {
        "profile_user": target_user,
        "goals_by_age": sorted_goals_by_age,
        "active_age": active_age,
    })

@login_required
@require_http_methods(["GET", "POST"])
def goals_create(request):
    # ---- GET(最初の表示) ----
    if request.method == "GET":
        return render(request, 'goals/goal_create.html')
    # ---- POST（長期目標入力）----
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        limit_age_str = request.POST.get("limit_age")  # HTMLのinput type="date" で受け取る
        ctx = {"title": title, "limit_age_str": limit_age_str}
        # ---- 空欄チェック ----
        if not title:
            messages.error(request, "タイトルは必須です。")
            return render(request, "goals/goal_create.html", ctx)
        # ---- 文字数制限 ----
        if len(title) > 128:
            messages.error(request, "タイトルは128文字以内にしてください。")
            return render(request, "goals/goal_create.html", ctx)
        # ---- 期限の空欄チェック ----
        if not limit_age_str:
            messages.error(request, "期限を必ず設定してください。")
            return render(request, "goals/goal_create.html", ctx)
        # ---- 期限の形式チェック ----
        if limit_age_str:
            try:
                limit_age = datetime.strptime(limit_age_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "日付の形式が正しくありません。")
                return render(request, "goals/goal_create.html", ctx)
        # ---- 過去は設定できない ----
        today = timezone.localtime().date()
        if limit_age < today:
            messages.error(request, "過去の日付は選択できません。")
            return render(request, "goals/goal_create.html", ctx)
        
        # ---- 同じ年齢の目標は5個まで制限 ----
        birthday = request.user.birthday
        future_age = limit_age.year - birthday.year - (
            (limit_age.month, limit_age.day) < (birthday.month, birthday.day)
        )

        # 同じ future_age のゴールを数える
        count_same_age = 0
        for goal in GoalsModel.objects.filter(user=request.user):
            age = goal.limit_age.year - birthday.year - (
                (goal.limit_age.month, goal.limit_age.day) < (birthday.month, birthday.day)
            )
            if age == future_age:
                count_same_age += 1

        if count_same_age >= 5:
            messages.error(request, f"同じ年齢の目標は5件までしか登録できません。")
            return render(request, "goals/goal_create.html", ctx)

        # バリデーションOKなら保存
        goal = GoalsModel.objects.create(
            user=request.user,
            title=title,
            limit_age=limit_age,
        )
        messages.success(request, "目標を登録しました！")
        return redirect("goals:home")

@login_required
@require_http_methods(["GET", "POST"])   
def goals_edit(request, goal_id):
    goal = get_object_or_404(GoalsModel, id=goal_id, user=request.user)

    # ---- GET（最初の表示） ----
    if request.method == "GET":
       
        # CBに保存されているものを表示
        ctx = {"goal": goal, "title": goal.title, "limit_age": goal.limit_age.isoformat(),}
        return render(request, "goals/goal_edit.html", ctx)
		
	# ---- POST（送信されたとき） ----
    # strip() = 前後の空白スペース・改行を消す
    title = request.POST.get("title", "").strip()
    limit_age_str = request.POST.get("limit_age", "").strip()
    
    ctx = {"goal": goal, "title": title, "limit_age": limit_age_str}
    
    # ---- 空欄チェック ----
    if not title or not limit_age_str:
        messages.error(request, "タイトルと期限を入力してください")
        return render(request, "goals/goal_edit.html", ctx)

    # ---- 日付形式チェック ----
    try:
        limit_age = date.fromisoformat(limit_age_str)
    except ValueError:
        messages.error(request, "期限の日付形式が正しくありません。")
        return render(request, "goals/goal_edit.html", ctx)

    #（今日より過去の日付はだめ）
    today = timezone.localtime().date()
    if limit_age < today:
        messages.error(request, "今日以降の日付を選んでください")
        return render(request, "goals/goal_edit.html", ctx)

    # ---- 保存 ----
    goal.title = title
    goal.limit_age = limit_age
    goal.save()

    messages.success(request, "長期目標を更新しました")
    return redirect("goals:home")    

@login_required
@require_http_methods(["POST"])				
def goals_delete(request, goal_id):
    goal = get_object_or_404(GoalsModel, id=goal_id, user=request.user)
    goal.delete()
    messages.success(request, "長期目標を削除しました。")
    return redirect("goals:home")
    
@login_required
@require_http_methods(["GET", "POST"])	
def goals_detail(request, goal_id):
    goal = get_object_or_404(GoalsModel, id=goal_id, user=request.user)
    steps = StepsModel.objects.filter(goals=goal).order_by("id")  # ← goals（複数）に
    # ステップ数と完了数を取得
    total_steps = steps.count()
    completed_steps = steps.filter(is_done=True).count()

    # 割合を計算（ゼロ除算対策）
    progress_percent = int((completed_steps / total_steps) * 100) if total_steps > 0 else 0

    return render(request, "goals/goal_detail.html", {
        "goal": goal, 
        "steps": steps,
        "progress_percent": progress_percent,
        })

@login_required
@require_http_methods(["POST"])
def complete_goal(request, goal_id):
    goal = get_object_or_404(GoalsModel, id=goal_id, user=request.user)
    goal.is_done = not goal.is_done
    goal.save()
    # 長期目標が達成済みになったら紐づく全てのstepsを達成済みにする
    if goal.is_done is True:
        StepsModel.objects.filter(goals=goal).update(is_done=True)
    else:
        pass

    # 完了ボタン押した goal の future_age を取得
    birthday = request.user.birthday
    future_age = goal.limit_age.year - birthday.year - ((goal.limit_age.month, goal.limit_age.day) < (birthday.month, birthday.day))
    
    # redirect に GET パラメータを付与
    url = reverse("goals:home") + f"?active_age={future_age}"
    return redirect(url)

@login_required
@require_http_methods(['GET'])
def life_map(request):
    return render(request, "goals/life-map.html")
