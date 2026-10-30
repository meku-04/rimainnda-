from django.shortcuts import render, redirect
from datetime import date
from .models import Task
from django.db import models



def index(request):

    
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        deadline = request.POST.get("deadline") or None
        priority = request.POST.get("priority", "medium")
        description = request.POST.get("description", "").strip()
        image = request.FILES.get("image")

        Task.objects.create(
            title=title,
            deadline=deadline,
            priority=priority,
            description=description,
            importance=3,
            image=image,
        )

        return redirect("/?added=1")


    # 今日の日付を取得
    today = date.today()

    # URLから絞り込み条件を取得
    filter_type = request.GET.get("filter", "all")

    # 最初はすべての予定を取得
    tasks = Task.objects.all()

    # 絞り込み条件に応じて予定を選ぶ
    if filter_type == "incomplete":
        tasks = tasks.filter(completed=False)

    elif filter_type == "completed":
        tasks = tasks.filter(completed=True)

    elif filter_type == "today":
        tasks = tasks.filter(deadline=today)

    tasks = tasks.order_by(
    models.Case(
        models.When(priority="high", then=0),
        models.When(priority="medium", then=1),
        models.When(priority="low", then=2),
        output_field=models.IntegerField(),
    ),
    "deadline",
    )
    
    for task in tasks:

        # 期限切れかどうかを判定する
        task.is_overdue = (
            task.deadline is not None
            and task.deadline < date.today()
            and not task.completed
        )

    return render(
        request,
        "app/index.html",
        {
            "tasks": tasks,
            "today": today,
            "filter_type": filter_type,
        }
    )


def delete_task(request, id):

    task = Task.objects.get(id=id)

    task.delete()

    return redirect("/")

def edit_task(request, id):

    # 編集するタスクを取得
    task = Task.objects.get(id=id)

    if request.method == "POST":

        # タイトル
        task.title = request.POST.get("title", "").strip()

        # 期限
        task.deadline = request.POST.get("deadline") or None

        # 優先度
        task.priority = request.POST.get("priority", "medium")

        # 説明文
        task.description = request.POST.get("description", "").strip()

        # 写真
        new_image = request.FILES.get("image")

        if new_image:
            task.image = new_image

        # 変更をデータベースに保存
        task.save()

        # カード一覧へ戻る
        return redirect("/")

    return render(request, "app/edit.html", {"task": task})
def toggle_task(request, id):

    task = Task.objects.get(id=id)

    task.completed = not task.completed

    task.save()

    return redirect("/")