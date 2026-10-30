
from django.db import models


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("high", "高"),
        ("medium", "中"),
        ("low", "低"),
    ]

    IMPORTANCE_CHOICES = [
        (1, "1個"),
        (2, "2個"),
        (3, "3個"),
        (4, "4個"),
        (5, "5個"),
        (6, "6個"),
    ]

    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    notified = models.BooleanField(default=False)

    # これまで使っていた重要度
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    # カードに表示する詳細な説明
    description = models.TextField(blank=True)

    # カードに表示する画像
    image = models.ImageField(
        upload_to="task_images/",
        blank=True,
        null=True
    )

    # 火の玉の数（1〜6）
    importance = models.PositiveSmallIntegerField(
        choices=IMPORTANCE_CHOICES,
        default=3
    )
