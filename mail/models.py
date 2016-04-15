from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Message(models.Model):
    """
    A private message from user to user
    """
    subject = models.CharField(_("Subject"), max_length=120, blank=True)
    body = models.TextField(_("Body"))
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender_messages', verbose_name=_("Sender"), )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver_messages', null=True, blank=True, verbose_name=_("Recipient"))
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, verbose_name=_("Parent message"))
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
    sender_deleted_at = models.DateTimeField(_("Sender deleted at"), null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"), null=True, blank=True)
    ip = models.GenericIPAddressField(verbose_name=_('IP'), null=True, blank=True)
    user_agent = models.CharField(verbose_name=_('User Agent'), blank=True, max_length=255)

    def new(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True

    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False

    def __str__(self):
        if self.subject is not None:
            return self.subject
        if self.body is not None:
            return self.body[:40]
        return None

    def get_absolute_url(self):
        return reverse('messages_detail', args=[self.id])

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = now()
        super(Message, self).save(**kwargs)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")