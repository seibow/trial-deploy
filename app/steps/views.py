from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.goals.models import GoalsModel
from .models import StepsModel
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def step_create(request, goal_id):

    goal = get_object_or_404(GoalsModel, id=goal_id, user=request.user)

    # ---- GET(最初の表示) ----
    if request.method == "GET":
        return render(request, "steps/step_create.html", {"goal": goal})

    # ---- POST（スモールステップ入力）----
    title = request.POST.get("title", "").strip()
    ctx = {"goal": goal, "title": title}

    # ---- 空欄チェック ----
    if not title:
        messages.error(request, "タイトルは必須です。")
        return render(request, "steps/step_create.html", ctx)

    # ---- 文字数制限 ----
    if len(title) > 128:
        messages.error(request, "タイトルは128文字以内にしてください。")
        return render(request, "steps/step_create.html", ctx)

    # バリデーションOKなら保存
    StepsModel.objects.create(
        goals=goal,
        title=title,
        is_done=False,
    )

    messages.success(request, "スモールステップを追加しました！")
    return redirect("goals:goal_detail", goal_id=goal.id)

@login_required
@require_http_methods(["POST"])
def step_delete(request, step_id):
    step = get_object_or_404(StepsModel, id=step_id, goals__user=request.user)
    goal_id = step.goals.id
    step.delete()
    messages.success(request, "スモールステップを削除しました。")
    return redirect("goals:goal_detail", goal_id=goal_id)

@login_required
@require_http_methods(["POST"])
def complete_step(request, step_id):
    step = get_object_or_404(StepsModel, id=step_id, goals__user=request.user)
    goal = get_object_or_404(GoalsModel, id=step.goals.id, user=request.user)
    step.is_done = not step.is_done
    step.save()
    # stepをまた未達成に戻したら、長期目標も未達成に戻る
    if step.is_done is False:
        goal.is_done = False
        goal.save()
    return redirect("goals:goal_detail", goal_id=step.goals.id)

