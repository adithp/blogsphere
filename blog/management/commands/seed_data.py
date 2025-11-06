import os
import random
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from accounts.models import User
from blog.models import Category, Post, Comment, PostLike

class Command(BaseCommand):
    help = "Generate complete dummy data with CKEditor content and images"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Ensure media folders exist
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        thumb_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnail')
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(thumb_dir, exist_ok=True)

        # Helper function to download random placeholder images
        def download_image(save_dir, filename):
            url = f"https://picsum.photos/seed/{random.randint(1,1000)}/600/400"
            path = os.path.join(save_dir, filename)
            r = requests.get(url)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    f.write(r.content)
            return os.path.relpath(path, settings.MEDIA_ROOT)

        # Create Users
        if not User.objects.exists():
            self.stdout.write("👤 Creating users...")
            for i in range(5):
                User.objects.create(
                    username=fake.user_name(),
                    email=fake.email(),
                    password="1234"  # For dummy data only
                )

        users = list(User.objects.all())

        # Create Categories
        self.stdout.write("📂 Creating categories...")
        categories = [Category.objects.create(title=fake.word()) for _ in range(4)]

        # Create Posts
        self.stdout.write("📝 Creating posts with images and HTML...")
        for _ in range(10):
            # Download a random thumbnail
            thumb_filename = f"thumb_{random.randint(1,1000)}.jpg"
            thumb_path = download_image(thumb_dir, thumb_filename)

            # Create HTML-rich content
            content = f"""
                <h2>{fake.sentence()}</h2>
                <p>{fake.paragraph(nb_sentences=4)}</p>
                <p><strong>{fake.sentence()}</strong></p>
                <p><img src="/media/{download_image(upload_dir, f'img_{random.randint(1,1000)}.jpg')}" alt="Post image"></p>
                <p>{fake.paragraph(nb_sentences=3)}</p>
                <p>Check more on <a href="{fake.url()}">{fake.domain_name()}</a>.</p>
            """

            post = Post.objects.create(
                author=random.choice(users),
                title=fake.sentence(nb_words=5),
                content=content,
                thumbnail=f"thumbnail/{thumb_filename}",
                slug=fake.slug(),
                category=random.choice(categories)
            )

            # Add random likes
            for _ in range(random.randint(1, 5)):
                PostLike.objects.create(user=random.choice(users), post=post)

            # Add random comments
            for _ in range(random.randint(1, 5)):
                Comment.objects.create(
                    user=random.choice(users),
                    post=post,
                    content=fake.sentence(),
                    is_deleted=False
                )

        self.stdout.write(self.style.SUCCESS("✅ Full dummy data generated successfully!"))
