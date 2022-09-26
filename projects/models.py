from asyncio import trsock
from django.db import models
import uuid
from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.png')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        # میگه که اول بر اساس مثبت بودن رای بعد برا اساس تعداد رای ها
        ordering = ['-vote_ratio','-vote_total','title']

    @property
    def reviewers(self):
        #  ایدی تمام نظر دهنده ها رو به صورت لیست بده(flat)
        queryset = self.review_set.all().values_list('owner__id',flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVote = reviews.filter(value='up').count()
        # تعداد کوئری هایی که دارم را میگویید
        totalVotes = reviews.count()

        ratio = (upVote/totalVotes)*100


        self.vote_total = totalVotes
        self.vote_ratio = ratio
        
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        # باعث میشه که هیچ نظری مالک و پروژه مشابهی نداشته باشد
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
