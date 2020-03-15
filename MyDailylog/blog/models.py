from django.db import models
from django.utils import timezone
from django.urls import reverse

# 데이터베이스에 저장해둬야하는 Post와 comment는 어떤 개체로 구성될 것인지 modeling을 해야 한다.

class Post(models.Model): # Post는 author, title, text, created_date, published_date로 구성된다.
    author=models.ForeignKey('auth.User', on_delete=models.CASCADE) # author는 파이썬 auth에 있는 User를 외래키로 사용한다.
    title=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now) # created_date는 기본적으로 현재 시간으로 지정된다.
    published_date=models.DateTimeField(blank=True, null=True) # published_date는 후에 publish버튼을 누르면 시간이 지정된다.

    def publish(self): # Post를 publish하는 함수. published_date의 시간을 현재로 지정해준다.
        self.published_date=timezone.now()
        self.save()

    def get_absolute_url(self): # CreateView와 UpdateView에 success_url을 제공하지 않기 때문에 get_absolute_url을 통해 Create, Update작업 후 post_detail.view로 이동하도록 해준다.
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self): # 문자열로 어떻게 표현될 것인지 결정해준다.
        return self.title

    def approve_comments(self): # approved상태의 comment를 모은다.
        return self.comments.filter(approved_comment=True)

class Comment(models.Model): # Comment는 post, author, text, created_date, approved_comment로 구성된다.
    post=models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE) # 위에서 정의한 Post모델을 외래키로 쓴다. Post에 comment가 종속되는 형식이기 때문이다.
    author=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    approved_comment=models.BooleanField(default=False)

    def approve(self): # comment를 approve하는 함수
        self.approved_comment=True # 위의 Comment모델 구성요소 중 approved_comment의 상태를 False(default)에서 True로 바꾼다.
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
