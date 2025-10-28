from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from .models import Member

User = get_user_model()

@receiver(post_save, sender=Member)
def create_user_for_member(sender, instance, created, **kwargs):
    """Automatically create a User for a new Member.

    - Username = member.member_id
    - Sets a default password and flags `must_change_password` so admin can force change on first login.
    - Sends password reset email to member.email so they can set their own password.

    Note: This triggers only when a Member is created and member.user is None.
    """
    if not created:
        return
    if instance.user is not None:
        return

    # avoid creating duplicate users
    existing = User.objects.filter(username=instance.member_id).first()
    if existing:
        instance.user = existing
        instance.save(update_fields=['user'])
        return

    # create user with a simple default temporary password (should be changed on first login)
    temp_password = 'ChangeMe123!'
    user = User.objects.create_user(username=instance.member_id, email=instance.email or '', password=temp_password)
    user.is_active = True
    user.save()

    instance.user = user
    instance.must_change_password = True
    instance.save(update_fields=['user', 'must_change_password'])

    # send password reset link so the member can set a new password
    if instance.email:
        token = default_token_generator.make_token(user)
        uid = user.pk
        reset_path = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        reset_url = f"{settings.DEFAULT_FROM_EMAIL}{reset_path}"
        subject = 'Set your Saytaman account password'
        message = f"Hello {instance.name},\n\nAn account was created for you. Please set your password using the link below:\n{reset_url}\n\nIf you did not expect this, contact the site administrator.\n"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])
