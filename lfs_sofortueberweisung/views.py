import hashlib

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

import lfs
from lfs.order.models import Order
from lfs.order.settings import PAID


def success_notification(request, order_id, security_hash):
    order = get_object_or_404(Order, pk=order_id)

    key = '%s-%s-%s' % (settings.SECRET_KEY, order.pk, order.price)
    calculated_security_hash = hashlib.md5(key).hexdigest()

    if calculated_security_hash != security_hash:
        raise Http404

    order.state = PAID
    order.save()
    lfs.core.signals.order_paid.send({"order": order, "request": request})
    return redirect(reverse('lfs_thank_you'))