from django.contrib.postgres.fields import ArrayField
from django.db import models

from forge.models import TimestampModel, UUIDModel
from forgepro.stripe.models import StripeModel

from github import (
    add_deploy_key_to_repo,
    invite_username_to_repo,
    remove_deploy_key_from_repo,
    remove_username_from_repo,
)


class Project(TimestampModel, UUIDModel, StripeModel):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(
        "teams.Team", on_delete=models.CASCADE, related_name="projects"
    )
    # url?

    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    terms_accepted_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    pro_private_key = models.TextField(blank=True)
    pro_public_key = models.TextField(blank=True)

    # Person (people) who will be invited to repo for this project
    github_usernames = ArrayField(
        models.SlugField(max_length=255), blank=True, null=True
    )

    # Mostly used for the Stripe status
    status = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name

    def sync_stripe(self):
        subscription = self.get_stripe_object()
        if subscription:
            self.status = subscription.status
        else:
            self.status = ""
        self.save()

    def invite_github_usernames(self):
        for username in self.github_usernames:
            invite_username_to_repo(username)

    def remove_github_usernames(self):
        for username in self.github_usernames:
            has_other_projects = (
                Project.objects.exclude(id=self.id)
                .filter(status="active", github_usernames__icontains=username)
                .exists()
            )
            if not has_other_projects:
                remove_username_from_repo(username)

    def ensure_pro_keys(self):
        if not self.pro_private_key or not self.pro_public_key:
            self.create_pro_keys()

    def create_pro_keys(self):
        self.pro_private_key, self.pro_public_key = generate_ssh_key()
        add_deploy_key_to_repo(self.pro_public_key, f"project:{self.uuid}")
        self.save()

    def remove_pro_keys(self):
        remove_deploy_key_from_repo(self.pro_public_key)
        self.pro_private_key = ""
        self.pro_public_key = ""
        self.save()


def generate_ssh_key():
    from cryptography.hazmat.backends import default_backend as crypto_default_backend
    from cryptography.hazmat.primitives import serialization as crypto_serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption(),
    ).decode("utf-8")

    public_key = (
        key.public_key()
        .public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH,
        )
        .decode("utf-8")
    )

    return private_key, public_key
