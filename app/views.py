from django.contrib.auth.mixins import LoginRequiredMixin
from forge.views.mixins import HTMLTitleMixin
from forgepro.stripe.views import StripeWebhookView

from projects.models import Project


class BaseLoggedInViewMixin(LoginRequiredMixin, HTMLTitleMixin):
    pass


class StripeWebhookView(StripeWebhookView):
    def handle_stripe_event(self, event):
        if event.type == "checkout.session.completed":
            project_uuid = event.data.object.client_reference_id
            project = Project.objects.get(uuid=project_uuid)
            project.stripe_id = event.data.object.subscription
            project.save()

            project.sync_stripe()

            project.ensure_pro_keys()
            project.invite_github_usernames()

        elif event.type == "customer.subscription.deleted":
            subscription_id = event.data.object.id
            project = Project.objects.get(stripe_id=subscription_id)
            project.stripe_id = ""
            project.save()

            project.sync_stripe()

            project.remove_github_usernames()
            project.remove_pro_keys()
